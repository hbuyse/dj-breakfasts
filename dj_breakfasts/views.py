# coding=utf-8

"""Views."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.dates import (
    YearArchiveView
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
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
    past = False

    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        context['past'] = self.past
        return context

    def get_queryset(self):
        q = []
        if self.past:
            q = Breakfast.objects.filter(date__lte=datetime.today()).order_by("date")
        else:
            q = Breakfast.objects.filter(date__gt=datetime.today()).order_by("-date")
        
        return q

class BreakfastDetailView(DetailView):
    model = Breakfast

class BreakfastCreateView(CreateView):
    model = Breakfast
    success_url = reverse_lazy('dj-breakfasts:next')
    form_class = BreakfastForm

class BreakfastUpdateView(UpdateView):
    model = Breakfast
    fields = "__all__"
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('dj-breakfasts:detail', args = (self.object.id,))

class BreakfastDeleteView(DeleteView):
    model = Breakfast
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('dj-breakfasts:next')

class ParticipantListView(ListView):
    model = Participant

    def get_queryset(self):
        q = Participant.objects.all()

        if self.request.user.is_anonymous:
            q = q.filter(is_active=True)

        return q

class ParticipantDetailView(DetailView):
    model = Participant

class ParticipantCreateView(CreateView):
    model = Participant
    fields = ['first_name',
        'last_name',
        'email'
        ]
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('dj-breakfasts:participant-detail', args = (self.object.id,))

class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = ['first_name',
        'last_name',
        'email'
        ]
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('dj-breakfasts:participant-detail', args = (self.object.id,))

class ParticipantDeleteView(DeleteView):
    model = Participant
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('dj-breakfasts:participant-list')
