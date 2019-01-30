# -*- coding: utf-8
"""Representation of the breakfasts application and its configuration."""

import logging

# Django
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class BreakfastsConfig(AppConfig):
    """Representation of the breakfasts application and its configuration."""

    name = 'breakfasts'

    def ready(self):
        logger.debug("App {} ready.".format(self.name))
