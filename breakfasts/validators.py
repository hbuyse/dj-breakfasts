from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def date_is_future(value):
    """Validator to check if the value is in the future."""
    if isinstance(value, datetime):
        if value <= timezone.now():
            raise ValidationError(_("The date entered must be greater than today."))
    elif isinstance(value, date):
        if value <= date.today():
            raise ValidationError(_("The date entered must be greater than today."))
    else:
        raise ValidationError(_("The value entered isn't a valid type of date or datetime."))


def date_is_present_or_future(value):
    """Validator to check if the value is today or in the future."""
    if isinstance(value, datetime):
        if value < timezone.now():
            raise ValidationError(_("The date entered must be today or greater."))
    elif isinstance(value, date):
        if value < date.today():
            raise ValidationError(_("The date entered must be today or greater."))
    else:
        raise ValidationError(_("The value entered isn't a valid type of date or datetime."))
