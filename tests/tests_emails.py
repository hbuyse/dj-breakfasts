#!/usr/bin/env python
# coding=utf-8

"""Tests for `breakfasts` models module."""

from breakfasts.emails import send_deferred_mail
from datetime import date
from django.test import TestCase, override_settings

class TestSendingDeferredEmail(TestCase):
    """Test deferred email sending."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.testing_array = [
            {
                'recipient': None,
                'first_name': None,
                'date': None,
                'result': False
            },
            {
                'recipient': None,
                'first_name': None,
                'date': date.today(),
                'result': False
            },
            {
                'recipient': None,
                'first_name': 'Toto',
                'date': None,
                'result': False
            },
            {
                'recipient': 'toto@toto.com',
                'first_name': None,
                'date': None,
                'result': False
            },
            {
                'recipient': 'toto@toto.com',
                'first_name': 'Toto',
                'date': date.today(),
                'result': True
            }
        ]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_deferred_email(self):
        for testing in self.testing_array:
            self.assertEqual(testing['result'], send_deferred_mail(testing['recipient'], testing['first_name'], testing['date']))
