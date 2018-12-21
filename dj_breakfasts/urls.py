# coding=utf-8

"""urls for the dj-breakfasts package."""

from datetime import datetime

from django.urls import path, reverse
from django.views.generic.base import RedirectView

from . import views


app_name = 'dj-breakfasts'
urlpatterns = [
    path("",
         view=RedirectView.as_view(url="list/"),
         name='index',
         ),
    path("list/",
         view=views.BreakfastListView.as_view(),
         name="list"
         ),
    path("create/",
         view=views.BreakfastCreateView.as_view(),
         name="create"
         ),
    path("<int:year>/",
         view=views.BreakfastYearArchiveView.as_view(),
         name="year"
         ),
    path("participants/",
         view=views.ParticipantListView.as_view(),
         name="participant-list"
         ),
    path("participants/<int:pk>",
         view=views.ParticipantDetailView.as_view(),
         name="participant-detail"
         ),
    path("participants/create",
         view=views.ParticipantCreateView.as_view(),
         name="participant-create"
         ),
]
