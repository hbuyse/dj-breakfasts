# -*- coding: utf-8
"""Representation of the gymnasiums application and its configuration."""

# Django
from django.apps import AppConfig


class BreakfastsConfig(AppConfig):
    """Representation of the gymnasiums application and its configuration."""

    name = 'breakfasts'

    def ready(self):
        """Code ran when django starts."""
        import breakfasts.signals   # noqa
