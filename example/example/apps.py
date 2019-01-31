# -*- coding: utf-8
"""Representation of the main application and its configuration."""

import logging

# Django
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class ExampleConfig(AppConfig):
    """Representation of the main application and its configuration."""

    name = "example"

    def ready(self):
        """Import the signal handlers when Django starts."""
        logger.debug("App {} ready.".format(self.name))
        import example.handlers
