#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from breakfasts.models import Breakfast, Participant

@override_settings(LOGIN_URL="/toto/")
class TestBreakfastUpdateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast = cls.participant.breakfast_set.last()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/toto/", r.url)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        r = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("/toto/", r.url)


class TestBreakfastUpdateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        cls.user = get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast = cls.participant.breakfast_set.last()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))


class TestBreakfastUpdateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        cls.staff = get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast = cls.participant.breakfast_set.last()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))


class TestBreakfastUpdateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        cls.superuser = get_user_model().objects.create_superuser(**cls.dict)
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast = cls.participant.breakfast_set.last()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))
