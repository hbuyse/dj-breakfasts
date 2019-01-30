#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Standard library
from datetime import date, timedelta

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase, tag
from django.urls import reverse

# Current django project
from breakfasts.models import Breakfast, Participant


@tag('breakfast', 'view', 'list', 'past', 'anonymous')
class TestBreakfastListViewPastAsAnonymous(TestCase):
    """Tests ListView for Post."""

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        participant = Participant.objects.create()
        Breakfast.objects.create(participant=participant, date=date.today())

        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        participant = Participant.objects.create()
        for i in range(1, 11):
            Breakfast.objects.create(participant=participant, date=date.today() - timedelta(days=i))

        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'past', 'logged')
class TestBreakfastListViewPastAsLogged(TestCase):
    """Tests ListView for Post.

    Note: there is at least one user active in this test. It is the one created in the setUp method.
    """

    def setUp(self):
        """Create a user that will be able to log in."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        participant = Participant.objects.create()
        Breakfast.objects.create(participant=participant, date=date.today())

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        participant = Participant.objects.create()
        for i in range(1, 11):
            Breakfast.objects.create(participant=participant, date=date.today() - timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'past', 'staff')
class TestBreakfastListViewPastAsStaff(TestCase):
    """Tests ListView for Post."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        self.staff = get_user_model().objects.create_user(**self.dict)

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        participant = Participant.objects.create()
        Breakfast.objects.create(participant=participant, date=date.today())

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        participant = Participant.objects.create()
        for i in range(1, 11):
            Breakfast.objects.create(participant=participant, date=date.today() - timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'past', 'superuser')
class TestBreakfastListViewPastAsSuperuser(TestCase):
    """Tests ListView for Post."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.dict)

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        participant = Participant.objects.create()
        Breakfast.objects.create(participant=participant, date=date.today())

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        participant = Participant.objects.create()
        for i in range(1, 11):
            Breakfast.objects.create(participant=participant, date=date.today() - timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:past'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)
