# -*- coding: utf-8
"""..."""

# Standard library
from datetime import timedelta

# Django
from django.contrib import admin

# Current django project
from breakfasts.models import Breakfast, Participant


@admin.register(Breakfast)
class BreakfastAdmin(admin.ModelAdmin):
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
        for obj in queryset:
            obj.date += timedelta(7)
            obj.save()

    def invert_two_participants(self, request, queryset):
        if len(queryset) != 2:
            self.message_user(request, "Impossible to invert {} participants".format(len(queryset)))
        else:
            queryset[0].date, queryset[1].date = queryset[1].date, queryset[0].date
            for b in queryset:
                b.save()


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Participant admin object."""

    list_display = (
        'first_name',
        'last_name'
    )
