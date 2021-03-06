# -*- coding: utf-8
"""Project forms."""

# Standard library
import logging
from datetime import datetime

# Django
from django.forms import CheckboxSelectMultiple, DateInput, Form, ModelChoiceField, ModelForm, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

# Current django project
from breakfasts.models import Breakfast, Participant
from breakfasts.validators import only_two_items_in_list

logger = logging.getLogger(__name__)


class BreakfastForm(ModelForm):
    """Form for creating a new assignment for a course."""

    participant = ModelChoiceField(
        queryset=Participant.objects.filter(is_active=True),
        empty_label=None,
        help_text=_('Participant that has to pay')
    )

    class Meta:

        model = Breakfast
        widgets = {
            "date": DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        }
        help_texts = {
            'date': _('The date has to be in the future'),
        }
        fields = ['date', 'participant']


class BreakfastMultipleChoiceField(ModelMultipleChoiceField):
    """Override ModelMultipleChoiceField in order to change the method label_from_instance."""

    def label_from_instance(self, obj):
        """Override label_from_instance in order to the label."""
        return "{}: {} {}".format(obj.date, obj.participant.first_name, obj.participant.last_name)


class BreakfastAlternateForm(Form):
    """Form to alternate participants between two breakfasts."""

    breakfast_list = BreakfastMultipleChoiceField(
        queryset=Breakfast.objects.filter(date__gt=datetime.today()).order_by("date"),
        widget=CheckboxSelectMultiple,
        label=_("Select two breakfasts to alternate the participants"),
        validators=[only_two_items_in_list]
    )
