# -*- coding: utf-8

# Standard library
from datetime import date, timedelta

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

# Local Django
from breakfasts.forms import BreakfastForm, BreakfastAlternateForm
from breakfasts.models import Breakfast, Participant



class TestBreakfastForm(TestCase):
    """Form to alternate participants between two breakfasts."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_empty(self):
        form_data = {}
        form = BreakfastForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_date(self):
        form_data = {
            'date': Breakfast.objects.last().date + timedelta(weeks=1)
        }
        form = BreakfastForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_participant(self):
        form_data = {
            'participant': self.participant.id
        }
        form = BreakfastForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_date_in_past_and_participant(self):
        form_data = {
            'date': date.today() - timedelta(weeks=1),
            'participant': self.participant.id
        }
        form = BreakfastForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_date_is_today_and_participant(self):
        form_data = {
            'date': date.today(),
            'participant': self.participant.id
        }
        form = BreakfastForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_date_in_future_and_participant(self):
        form_data = {
            'date': Breakfast.objects.last().date + timedelta(days=1),
            'participant': self.participant.id
        }
        form = BreakfastForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestBreakfastAlternateForm(TestCase):
    """Form to alternate participants between two breakfasts."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.participant_1 = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.participant_2 = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_empty_form(self):
        form_data = {}
        form = BreakfastAlternateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_list(self):
        form_data = {
            'breakfast_list': []
        }
        form = BreakfastAlternateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_one_item_list(self):
        form_data = {
            'breakfast_list': ["1"]
        }
        form = BreakfastAlternateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_three_items_list(self):
        Breakfast.objects.create(
            participant=self.participant_1,
            date=Breakfast.objects.last().date + timedelta(weeks=1)
            )
        form_data = {
            'breakfast_list': ["1", "2", "3"]
        }
        form = BreakfastAlternateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_two_items_list(self):
        form_data = {
            'breakfast_list': ["1", "2"]
        }
        form = BreakfastAlternateForm(data=form_data)
        self.assertTrue(form.is_valid())
