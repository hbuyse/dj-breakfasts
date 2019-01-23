#!/usr/bin/env python
# coding=utf-8

"""Tests for `breakfasts` models module."""

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from breakfasts.validators import date_is_future, date_is_present_or_future, only_two_items_in_list

class TestDateIsFuture(TestCase):
    """Test date_is_future validator."""

    def test_date_is_past(self):
        """Test date_is_future validator in the past."""
        self.assertRaises(ValidationError, date_is_future, date.today() - timedelta(days=1))
        self.assertRaises(ValidationError, date_is_future, timezone.now() - timedelta(days=1))

    def test_date_is_today(self):
        """Test date_is_future validator now."""
        self.assertRaises(ValidationError, date_is_future, date.today())
        self.assertRaises(ValidationError, date_is_future, timezone.now())

    def test_date_is_future(self):
        """Test date_is_future validator in the future."""
        date_is_future(date.today() + timedelta(days=1))
        date_is_future(timezone.now() + timedelta(days=1))

    def test_wrong_type(self):
        """Test date_is_future validator with a wrong type of value"""
        self.assertRaises(ValidationError, date_is_future, str())
        self.assertRaises(ValidationError, date_is_future, int())


class TestDateIsPresentOrFuture(TestCase):
    """Test date_is_present_or_future validator."""

    def test_past(self):
        """Test date_is_present_or_future validator in the past."""
        self.assertRaises(ValidationError, date_is_present_or_future, date.today() - timedelta(days=1))
        self.assertRaises(ValidationError, date_is_present_or_future, timezone.now() - timedelta(days=1))

    def test_present(self):
        """Test date_is_present_or_future validator now.

        We add one second when using timezone because the test fails otherwise.
        """
        date_is_present_or_future(date.today())
        date_is_present_or_future(timezone.now() + timedelta(seconds=1))

    def test_future(self):
        """Test date_is_present_or_future validator in the future."""
        date_is_present_or_future(date.today() + timedelta(days=1))
        date_is_present_or_future(timezone.now() + timedelta(days=1))

    def test_wrong_type(self):
        """Test date_is_present_or_future validator with a wrong type of value"""
        self.assertRaises(ValidationError, date_is_present_or_future, str())
        self.assertRaises(ValidationError, date_is_present_or_future, int())


class TestOnlyTwoItemsInList(TestCase):
    """Test only_two_items_in_list validator."""

    def test_wrong_list_len(self):
        """Test only_two_items_in_list validator with wrong list length."""
        lists = [
            [],
            [1],
            [1, 2, 3]
        ]
        for l in lists:
            self.assertRaises(ValidationError, only_two_items_in_list, l)

    def test_correct_list_len(self):
        """Test only_two_items_in_list validator with correct list length."""
        only_two_items_in_list([1, 2])

    def test_wrong_type(self):
        """Test only_two_items_in_list validator with a wrong type of value"""
        types = [None, str(), dict(), int()]
        for i_type in types:
            self.assertRaises(ValidationError, only_two_items_in_list, i_type)
