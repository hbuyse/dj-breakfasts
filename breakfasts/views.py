# -*- coding: utf-8 -*-

"""Views."""

# Standard library
import logging
from datetime import datetime

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

# Current django project
from breakfasts.forms import BreakfastAlternateForm, BreakfastForm
from breakfasts.models import Breakfast, Participant

logger = logging.getLogger(__name__)


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


class BreakfastCreateView(LoginRequiredMixin, CreateView):
    model = Breakfast
    form_class = BreakfastForm

    def get_success_url(self):
        return reverse('breakfasts:detail', args=(self.object.id,))


class BreakfastUpdateView(LoginRequiredMixin, UpdateView):
    model = Breakfast
    form_class = BreakfastForm

    def get_success_url(self):
        return reverse('breakfasts:detail', args=(self.object.id,))


class BreakfastDeleteView(LoginRequiredMixin, DeleteView):
    model = Breakfast

    def get_success_url(self):
        return reverse('breakfasts:next')


class BreakfastAlternateView(LoginRequiredMixin, FormView):
    """Page to alternate breakfasts between two participants."""
    template_name = "breakfasts/breakfast_alternate.html"
    form_class = BreakfastAlternateForm

    def form_valid(self, form):
        """Alternate dates between two breakfasts."""
        data = form.clean()
        self.breakfast_list = data["breakfast_list"]
        self.breakfast_list[0].date, self.breakfast_list[1].date = self.breakfast_list[1].date, self.breakfast_list[0].date

        for b in self.breakfast_list:
            logger.info("Saving new date for breakfast {}".format(b.id))
            b.save()

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request,
            "Alternate two dates: {} and {}".format(self.breakfast_list[0].date, self.breakfast_list[1].date)
        )
        return reverse('breakfasts:next')


class ParticipantListView(ListView):
    model = Participant

    def get_queryset(self):
        q = Participant.objects.all()

        if self.request.user.is_anonymous:
            q = q.filter(is_active=True)

        return q


class ParticipantDetailView(DetailView):
    model = Participant


class ParticipantCreateView(LoginRequiredMixin, CreateView):
    model = Participant
    fields = [
        'first_name',
        'last_name',
        'email'
    ]

    def get_success_url(self):
        return reverse('breakfasts:participant-detail', args=(self.object.id,))


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    fields = [
        'first_name',
        'last_name',
        'email'
    ]

    def get_success_url(self):
        return reverse('breakfasts:participant-detail', args=(self.object.id,))


class ParticipantDeactivateView(LoginRequiredMixin, DeleteView):
    model = Participant
    template_name = "breakfasts/participant_confirm_deactivate.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('breakfasts:participant-list')
