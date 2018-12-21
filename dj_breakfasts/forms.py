from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import Breakfast, Participant

class BreakfastForm(forms.ModelForm):
    """
    Form for creating a new assignment for a course

    """
    date = forms.DateField(
                widget=SelectDateWidget(
                    empty_label=("Choose Year", "Choose Month", "Choose Day"),
                ),
            )
    participant = forms.ModelChoiceField(queryset=Participant.objects, empty_label=None)
        
    class Meta:
        model = Breakfast
        fields = "__all__"