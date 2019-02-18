# -*- coding: utf-8 -*-
"""Validators for the `breakfasts` project."""

# Standard library
from datetime import date, datetime

# Django
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def date_is_future(value):
    """Check if the value is in the future."""
    if isinstance(value, datetime):
        if value <= timezone.now():
            raise ValidationError(_("The date entered must be greater than today."))
    elif isinstance(value, date):
        if value <= date.today():
            raise ValidationError(_("The date entered must be greater than today."))
    else:
        raise ValidationError(_("The value entered isn't a valid type of date or datetime."))


def date_is_present_or_future(value):
    """Check if the value is today or in the future."""
    if isinstance(value, datetime):
        if value < timezone.now():
            raise ValidationError(_("The date entered must be today or greater."))
    elif isinstance(value, date):
        if value < date.today():
            raise ValidationError(_("The date entered must be today or greater."))
    else:
        raise ValidationError(_("The value entered isn't a valid type of date or datetime."))


def only_two_items_in_list(value):
    """Check that there are only two items in the given list."""
    if value is None:
        raise ValidationError(_("Breakfast list cannot be None."))
    elif not isinstance(value, list):
        raise ValidationError(_("Breakfast list has to be a list."))
    elif len(value) != 2:
        raise ValidationError(_("You have to select two breakfast dates to alternate."))
