# -*- coding: utf-8 -*-

"""urls for the breakfasts package."""

# Django
from django.urls import path
from django.views.generic.base import RedirectView

# Current django project
from breakfasts import views

app_name = 'breakfasts'
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
    path("alternate/",
         view=views.BreakfastAlternateView.as_view(),
         name="alternate"
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
    path("participants/<int:pk>/deactivate/",
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
