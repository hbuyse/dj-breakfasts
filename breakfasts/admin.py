# -*- coding: utf-8
"""Administrative representation of the `breakfasts` models."""

# Standard library
from datetime import timedelta

# Django
from django.contrib.admin import ModelAdmin, register

# Current django project
from breakfasts.models import Breakfast, Participant


@register(Breakfast)
class BreakfastAdmin(ModelAdmin):
    """Breakfast admin object."""

    list_display = (
        'date',
        'participant'
    )
    ordering = [
        'date'
    ]
    actions = [
        'shift_by_one_week',
        'invert_two_participants',
        'send_mail',
    ]

    def shift_by_one_week(self, request, queryset):
        """Shift all the breakfasts by one week."""
        for obj in queryset:
            obj.date += timedelta(weeks=1)
            obj.save()


@register(Participant)
class ParticipantAdmin(ModelAdmin):
    """Participant admin object."""

    list_display = (
        'first_name',
        'last_name'
    )
