# coding=utf-8

"""urls for the dj-breakfasts package."""

from datetime import datetime

from django.urls import path, reverse
from django.views.generic.base import RedirectView

from . import views


app_name = 'dj-breakfasts'
urlpatterns = [
    path("",
         view=RedirectView.as_view(url="next/"),
         name='index',
         ),
    path("next/",
         view=views.BreakfastListView.as_view(),
         name="next"
         ),
    path("past/",
         view=views.BreakfastListView.as_view(past=True),
         name="past"
         ),
    path("create/",
         view=views.BreakfastCreateView.as_view(),
         name="create"
         ),
    path("<int:pk>/",
         view=views.BreakfastDetailView.as_view(),
         name="detail"
         ),
    path("<int:pk>/update/",
         view=views.BreakfastUpdateView.as_view(),
         name="update"
         ),
    path("<int:pk>/delete/",
         view=views.BreakfastDeleteView.as_view(),
         name="delete"
         ),
    path("participants/<int:pk>/",
         view=views.ParticipantDetailView.as_view(),
         name="participant-detail"
         ),
    path("participants/<int:pk>/update/",
         view=views.ParticipantUpdateView.as_view(),
         name="participant-update"
         ),
    path("participants/<int:pk>/delete/",
         view=views.ParticipantDeactivateView.as_view(),
         name="participant-deactivate"
         ),
    path("participants/",
         view=views.ParticipantListView.as_view(),
         name="participant-list"
         ),
    path("participants/create/",
         view=views.ParticipantCreateView.as_view(),
         name="participant-create"
         ),
]
