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


@tag('breakfast', 'view', 'list', 'next', 'anonymous')
class TestBreakfastListViewNextAsAnonymous(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(weeks=1))

        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(1, 11):
            Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(days=i))

        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'next', 'logged')
class TestBreakfastListViewNextAsLogged(TestCase):
    """Tests ListView for Post.

    Note: there is at least one user active in this test. It is the one created in the setUp method.
    """

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        cls.user = get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create()

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(weeks=1))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(1, 11):
            Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'next', 'staff')
class TestBreakfastListViewNextAsStaff(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        cls.staff = get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create()

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(weeks=1))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(1, 11):
            Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


@tag('breakfast', 'view', 'list', 'next', 'superuser')
class TestBreakfastListViewNextAsSuperuser(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        cls.superuser = get_user_model().objects.create_superuser(**cls.dict)
        cls.participant = Participant.objects.create()

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(weeks=1))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(1, 11):
            Breakfast.objects.create(participant=self.participant, date=date.today() + timedelta(days=i))

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:next'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)
