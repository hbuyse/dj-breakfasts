# -*- coding: utf-8 -*-
"""Django Breakfast model implementation."""

from datetime import datetime, timedelta
from django.db import models
from django.core.mail import EmailMessage
from django.core.validators import RegexValidator
from django.template.loader import render_to_string, get_template
from django.utils.translation import gettext_lazy as _

from .tasks import send_deferred_mail_task

class Participant(models.Model):

    first_name = models.CharField(_('First name'), max_length=128)
    last_name  = models.CharField(_('Last name'), max_length=128)
    email = models.EmailField(_("Email"), max_length=254)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    modified = models.DateTimeField('Last modification date', auto_now=True)
    is_active = models.BooleanField(_("Is active"), default=True)

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

    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, unique_for_date="date")
    date = models.DateField('Breakfast creation date')
    created = models.DateTimeField('Breakfast creation date', auto_now_add=True)
    modified = models.DateTimeField('Breakfast last modification date', auto_now=True)
    email_task_id = models.CharField('Breakfast task_id', max_length=255)

    def __str__(self):
        """String representation."""
        return "Breakfast date {}".format(self.date)

    class Meta:
        """Meta class."""

        verbose_name = _("Breakfast date")
        verbose_name_plural = _("Breakfast dates")
        ordering = ("date",)
