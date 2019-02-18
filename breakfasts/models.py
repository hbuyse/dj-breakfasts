# -*- coding: utf-8 -*-
"""Django Breakfast model implementation."""

# Standard library
from datetime import datetime

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Current django project
from breakfasts.validators import date_is_future


class Participant(models.Model):
    """Participant model."""

    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)
    email = models.EmailField(_("email"), max_length=254)
    created = models.DateTimeField(_('creation date'), auto_now_add=True)
    modified = models.DateTimeField(_('last modification date'), auto_now=True)
    is_active = models.BooleanField(_("is active"), default=True)
    notif = models.BooleanField(_("receive email notification"), default=True)

    def __str__(self):
        """Representation as a string."""
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _("participant")
        ordering = ("first_name", "last_name")

    def get_past_breakfast(self):
        """Retrieve the list of the past breakfasts of a participant."""
        return self.breakfast_set.filter(date__lte=datetime.today()).order_by("-date")

    def get_future_breakfast(self):
        """Retrieve the list of the future breakfasts of a participant."""
        return self.breakfast_set.filter(date__gt=datetime.today()).order_by("date")

    def get_next_breakfast(self):
        """Retrieve the next breakfast of a participant."""
        return self.breakfast_set.filter(date__gt=datetime.today()).order_by("date").first()


class Breakfast(models.Model):
    """Breakfast model."""

    participant = models.ForeignKey('Participant', on_delete=models.DO_NOTHING, unique_for_date="date")
    date = models.DateField('date', validators=[date_is_future])
    created = models.DateTimeField(_("creation date"), auto_now_add=True)
    modified = models.DateTimeField(_("last modification date"), auto_now=True)
    email_task_id = models.CharField(_("email task id"), max_length=255, editable=False, blank=True)
    is_recursive = models.BooleanField(_("is recursive"), default=True)
    next_breakfast_task_id = models.CharField(_("next breakfast task id"), max_length=255, editable=False, blank=True)

    def __str__(self):
        """Representation as a string."""
        return _("Breakfast date %(date)s") % { "date": self.date }

    class Meta:
        verbose_name = _("breakfast")
        ordering = ("date",)
