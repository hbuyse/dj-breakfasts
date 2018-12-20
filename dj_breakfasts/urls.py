# coding=utf-8

"""urls for the dj-breakfasts package."""

from datetime import datetime

from django.urls import path
from django.views.generic.base import RedirectView

from . import views


app_name = 'dj-breakfasts'
urlpatterns = [
    path("",
         view=RedirectView.as_view(url='{}/'.format(datetime.now().year)),
         name='index',
         ),
    path("<int:year>/",
         view=views.BreakfastYearArchiveView.as_view(),
         name="breakfast_year"
         ),
]
