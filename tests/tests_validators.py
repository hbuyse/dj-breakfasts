#!/usr/bin/env python
# coding=utf-8

"""Tests for `breakfasts` models module."""

from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from breakfasts.validators import date_is_future, date_is_present_or_future

class TestDateIsFuture(TestCase):
    """Test Participant model."""

    def test_date_is_past(self):
        d = date.today() - timedelta(days=1)
        self.assertRaises(ValidationError, date_is_future, d)

    def test_date_is_today(self):
        d = date.today()
        self.assertRaises(ValidationError, date_is_future, d)

    def test_date_is_future(self):
        d = date.today() + timedelta(days=1)
        date_is_future(d)


class TestDateIsPresentOrFuture(TestCase):
    """Test Participant model."""

    def test_date_is_past(self):
        d = date.today() - timedelta(days=1)
        self.assertRaises(ValidationError, date_is_present_or_future, d)

    def test_date_is_today(self):
        d = date.today()
        date_is_present_or_future(d)

    def test_date_is_future(self):
        d = date.today() + timedelta(days=1)
        date_is_present_or_future(d)
