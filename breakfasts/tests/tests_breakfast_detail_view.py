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


@tag('breakfast', 'view', 'detail', 'anonymous')
class TestBreakfastDetailViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))
        self.assertEqual(r.status_code, 200)



@tag('breakfast', 'view', 'detail', 'logged')
class TestBreakfastDetailViewAsLogged(TestCase):
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
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))
        self.assertEqual(r.status_code, 200)



@tag('breakfast', 'view', 'detail', 'staff')
class TestBreakfastDetailViewAsStaff(TestCase):
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
        r = self.client.get(reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(r.status_code, 200)



@tag('breakfast', 'view', 'detail', 'superuser')
class TestBreakfastDetailViewAsSuperuser(TestCase):
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
        cls.participant = Participant.objects.create()
        cls.breakfast = Breakfast.objects.create(participant=cls.participant, date=date.today() + timedelta(weeks=1))

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:detail', kwargs={'pk': self.breakfast.id}))

        self.assertEqual(r.status_code, 200)
