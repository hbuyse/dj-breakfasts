#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Standard library
from datetime import date, timedelta

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings, tag
from django.urls import reverse

# Current django project
from breakfasts.models import Breakfast, Participant


@override_settings(LOGIN_URL="/toto/")
@tag('breakfast', 'view', 'update', 'anonymous')
class TestBreakfastUpdateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        response = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertRedirects(response, '/toto/?next=/{id}/update/'.format(id=self.breakfast.id), fetch_redirect_response=False)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        response = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertRedirects(response, '/toto/?next=/{id}/update/'.format(id=self.breakfast.id), fetch_redirect_response=False)


@tag('breakfast', 'view', 'update', 'logged')
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
        cls.useresponse = get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))


@tag('breakfast', 'view', 'update', 'staff')
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
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))


@tag('breakfast', 'view', 'update', 'superuser')
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
        cls.superuseresponse = get_user_model().objects.create_superuser(**cls.dict)
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'date': self.breakfast.date + timedelta(weeks=1),
            'participant': self.breakfast.participant.id
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:update', kwargs={'pk': self.breakfast.id}), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))
