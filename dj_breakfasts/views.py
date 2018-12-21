# coding=utf-8

"""Views."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic.dates import (
    YearArchiveView
)
from django.views.generic import (
    ListView,
    CreateView,
    DetailView
)
from .models import (
    Breakfast,
    Participant,
)
from .forms import (
    BreakfastForm
)

from datetime import datetime


class BreakfastYearArchiveView(YearArchiveView):
    queryset = Breakfast.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True

class BreakfastListView(ListView):
    queryset = Breakfast.objects.filter(date__gt=datetime.today()).order_by("-date")

class BreakfastCreateView(CreateView):
    model = Breakfast
    success_url = reverse_lazy('dj-breakfasts:list')
    form_class = BreakfastForm

class ParticipantListView(ListView):
    model = Participant

class ParticipantDetailView(DetailView):
    model = Participant

class ParticipantCreateView(CreateView):
    model = Participant
    success_url = reverse_lazy('dj-breakfasts:participant-create')
    fields = "__all__"
