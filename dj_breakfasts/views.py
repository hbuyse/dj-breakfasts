# coding=utf-8

"""Views."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic.dates import (
    YearArchiveView,
    MonthArchiveView,
)

from .models import (
    Breakfast
)


class BreakfastYearArchiveView(YearArchiveView):
    queryset = Breakfast.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True
