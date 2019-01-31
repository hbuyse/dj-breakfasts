# -*- coding: utf-8
"""Project forms."""

# Standard library
import logging
from datetime import datetime

# Django
from django.forms import CheckboxSelectMultiple, DateInput, Form, ModelChoiceField, ModelForm, ModelMultipleChoiceField

# Current django project
from breakfasts.models import Breakfast, Participant
from breakfasts.validators import only_two_items_in_list

logger = logging.getLogger(__name__)


class BreakfastForm(ModelForm):
    """Form for creating a new assignment for a course."""

    participant = ModelChoiceField(queryset=Participant.objects.filter(is_active=True), empty_label=None)

    class Meta:

        model = Breakfast
        widgets = {
            "date": DateInput(attrs={'class': 'form-control'}),
        }
        fields = ['date', 'participant']


class BreakfastAlternateForm(Form):
    """Form to alternate participants between two breakfasts."""

    breakfast_list = ModelMultipleChoiceField(
        queryset=Breakfast.objects.filter(date__gt=datetime.today()).order_by("date"),
        widget=CheckboxSelectMultiple,
        label="Select two breakfasts to alternate the participants",
        validators=[only_two_items_in_list]
    )