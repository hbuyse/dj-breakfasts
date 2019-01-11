# -*- coding: utf-8
from django.apps import AppConfig


class BreakfastsConfig(AppConfig):
    name = 'breakfasts'

    def ready(self):
        import breakfasts.signals
