# -*- coding: utf-8

# Django
from django.apps import AppConfig


class BreakfastsConfig(AppConfig):
    name = 'breakfasts'

    def ready(self):
        import breakfasts.signals
