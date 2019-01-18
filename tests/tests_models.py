#!/usr/bin/env python
# coding=utf-8

"""Tests for `breakfasts` models module."""

from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from breakfasts.models import (
    Breakfast,
    Participant
)

class TestParticipantModel(TestCase):
    """Test Participant model."""

    def setUp(self):
        """Setup function."""
        self.dict = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com',
        }

    def test_string_representation(self):
        """Test the string representation of the post model."""
        p = Participant(**self.dict)
        self.assertEqual(str(p), "{} {}".format(p.first_name, p.last_name))

    def test_verbose_name(self):
        """Test the verbose name in singular."""
        self.assertEqual(str(Participant._meta.verbose_name), "participant")

    def test_verbose_name_plural(self):
        """Test the verbose name in plural."""
        self.assertEqual(str(Participant._meta.verbose_name_plural), "participants")


class TestBreakfastModel(TestCase):
    """Test post class model."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_string_representation(self):
        """Test the string representation of the post model."""
        b = Breakfast(participant=self.participant, date=date.today())
        self.assertEqual(str(b), "Breakfast date {}".format(date.today()))

    def test_verbose_name(self):
        """Test the verbose name in singular."""
        self.assertEqual(str(Breakfast._meta.verbose_name), "Breakfast date")

    def test_verbose_name_plural(self):
        """Test the verbose name in plural."""
        self.assertEqual(str(Breakfast._meta.verbose_name_plural), "Breakfast dates")

    def test_date_is_in_the_past(self):
        b = Breakfast(participant=self.participant, date=date.today() - timedelta(days=1))
        self.assertRaises(ValidationError, b.full_clean)

    def test_date_is_today(self):
        b = Breakfast(participant=self.participant, date=date.today())
        self.assertRaises(ValidationError, b.full_clean)

    def test_date_is_tomorrow(self):
        b = Breakfast(participant=self.participant, date=date.today() + timedelta(days=1))
        b.full_clean()
