#!/usr/bin/env python
# coding=utf-8

"""
test_dj-sponsoring
------------

Tests for `dj-sponsoring` apps module.
"""

from breakfasts.apps import BreakfastsConfig

from django.apps import apps
from django.test import TestCase


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(BreakfastsConfig.name, 'breakfasts')
        self.assertEqual(apps.get_app_config('breakfasts').name, 'breakfasts')
