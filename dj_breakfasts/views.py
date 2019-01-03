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

from .tasks import send_deferred_mail

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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print(form.cleaned_data)
        send_deferred_mail.apply_async(
            (form.cleaned_data['participant'].email,
             form.cleaned_data['participant'].first_name,
             form.cleaned_data['date']
             ),
            countdown=60)
        return super().form_valid(form)

class ParticipantListView(ListView):
    model = Participant

class ParticipantDetailView(DetailView):
    model = Participant

class ParticipantCreateView(CreateView):
    model = Participant
    success_url = reverse_lazy('dj-breakfasts:participant-create')
    fields = "__all__"
