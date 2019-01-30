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
@tag('breakfast', 'view', 'create', 'anonymous')
class TestBreakfastCreateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for all the following tests."""
        cls.participant = Participant.objects.create()

    def test_get(self):
        """Tests."""
        response = self.client.get(reverse('breakfasts:create'))
        
        self.assertRedirects(response, "/toto/?next=/create/", fetch_redirect_response=False)


    def test_post_date_past(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() - timedelta(weeks=1)
        }
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertRedirects(response, "/toto/?next=/create/", fetch_redirect_response=False)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertRedirects(response, "/toto/?next=/create/", fetch_redirect_response=False)


@tag('breakfast', 'view', 'create', 'logged')
class TestBreakfastCreateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for all the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:create'))

        self.assertEqual(response.status_code, 200)

    def test_post_date_past(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() - timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Breakfast.objects.all()), 0)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(response.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 1)


@tag('breakfast', 'view', 'create', 'staff')
class TestBreakfastCreateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for all the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            "is_staff": True
        }
        get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:create'))

        self.assertEqual(response.status_code, 200)

    def test_post_date_past(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() - timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Breakfast.objects.all()), 0)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(response.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 1)


@tag('breakfast', 'view', 'create', 'superuser')
class TestBreakfastCreateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for all the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'henri.buyse@gmail.com'
        }
        get_user_model().objects.create_superuser(**cls.dict)
        cls.participant = Participant.objects.create()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.get(reverse('breakfasts:create'))

        self.assertEqual(response.status_code, 200)

    def test_post_date_past(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() - timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Breakfast.objects.all()), 0)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        response = self.client.post(reverse('breakfasts:create'), d)

        self.assertEqual(response.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(response.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 1)
