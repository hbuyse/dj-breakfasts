# -*- coding: utf-8

# Django
from django import forms

# Local Django
from breakfasts.models import Breakfast, Participant


class BreakfastForm(forms.ModelForm):
    """
    Form for creating a new assignment for a course

    """

    class Meta:
        model = Breakfast
        widgets = {
            "participant": forms.ModelChoiceField(queryset=Participant.objects, empty_label=None),
            "date": forms.DateInput(attrs={"class": "datepicker"}),
            }
        fields = [ 'date', 'participant' ]

class BreakfastAlternateForm(forms.Form):
    """Form to alternate participants between two breakfasts."""
    breakfast_list = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")
