from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import Breakfast, Participant
from .tasks import send_deferred_mail


class BreakfastForm(forms.ModelForm):
    """
    Form for creating a new assignment for a course

    """
    participant = forms.ModelChoiceField(queryset=Participant.objects, empty_label=None)
        
    class Meta:
        model = Breakfast
        widgets = {
            "participant": forms.ModelChoiceField(queryset=Participant.objects, empty_label=None),
            "date": forms.DateInput(attrs={"class": "datepicker"}),
            }
        fields = [ 'date', 'participant' ]
