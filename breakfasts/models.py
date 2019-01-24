# -*- coding: utf-8 -*-
"""Django Breakfast model implementation."""

# Standard library
from datetime import datetime

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Current django project
from breakfasts.validators import date_is_future


class Participant(models.Model):
    """Participant model."""

    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128)
    email = models.EmailField(_("email"), max_length=254)
    created = models.DateTimeField('creation date', auto_now_add=True)
    modified = models.DateTimeField('last modification date', auto_now=True)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        """String representation."""
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        """Meta class."""

        verbose_name = _("participant")
        verbose_name_plural = _("participants")
        ordering = ("first_name", "last_name")

    def get_past_breakfast(self):
        return self.breakfast_set.filter(date__lte=datetime.today()).order_by("-date")

    def get_future_breakfast(self):
        return self.breakfast_set.filter(date__gt=datetime.today()).order_by("date")

    def get_next_breakfast(self):
        return self.breakfast_set.filter(date__gt=datetime.today()).order_by("date").first()


class Breakfast(models.Model):
    """Breakfast date"""

    participant = models.ForeignKey('Participant', on_delete=models.DO_NOTHING, unique_for_date="date")
    date = models.DateField('breakfast creation date', validators=[date_is_future])
    created = models.DateTimeField('breakfast creation date', auto_now_add=True)
    modified = models.DateTimeField('breakfast last modification date', auto_now=True)
    email_task_id = models.CharField('breakfast task_id', max_length=255, editable=False, blank=True)

    def __str__(self):
        """String representation."""
        return "Breakfast date {}".format(self.date)

    class Meta:
        """Meta class."""

        verbose_name = _("Breakfast date")
        verbose_name_plural = _("Breakfast dates")
        ordering = ("date",)
