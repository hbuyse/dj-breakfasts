# -*- coding: utf-8

# Standard library
import logging
from datetime import datetime, date

# Django
from django.forms import (
    ModelForm, ModelChoiceField, Form, ModelMultipleChoiceField, CheckboxSelectMultiple, ValidationError, DateInput
)

# Local Django
from breakfasts.models import Breakfast, Participant

logger = logging.getLogger(__name__)

class BreakfastForm(ModelForm):
    """Form for creating a new assignment for a course."""

    participant = ModelChoiceField(queryset=Participant.objects.filter(is_active=True), empty_label=None)

    class Meta:
        model = Breakfast
        widgets = {
            "date": DateInput(attrs={"class": "datepicker"}),
            }
        fields = [ 'date', 'participant' ]

class BreakfastAlternateForm(Form):
    """Form to alternate participants between two breakfasts."""
    breakfast_list = ModelMultipleChoiceField(
        queryset=Breakfast.objects.filter(date__gt=datetime.today()).order_by("date"),
        widget=CheckboxSelectMultiple,
        label="Select two breakfasts to alternate the participants"
    )

    def clean(self):
        cleaned_data = super().clean()

        if "breakfast_list" not in cleaned_data:
            raise ValidationError("breakfast_list not in cleaned_data")
        elif len(cleaned_data["breakfast_list"]) != 2:
            raise ValidationError("You have to select two breakfast dates to alternate.")

        return cleaned_data