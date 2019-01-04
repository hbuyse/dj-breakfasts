# -*- coding: utf-8
from django.apps import AppConfig


class DjBreakfastsConfig(AppConfig):
    name = 'dj_breakfasts'

    def ready(self):
        import dj_breakfasts.signals
