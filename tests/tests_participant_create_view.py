#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from breakfasts.models import Participant


class TestParticipantCreateViewAsAnonymous(TestCase):
    """Tests."""

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:participant-create'))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/create/')

    def test_post(self):
        """Tests."""
        d = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        r = self.client.post(reverse('breakfasts:participant-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/create/')


class TestParticipantCreateViewAsLogged(TestCase):
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
        get_user_model().objects.create_user(**cls.dict)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-create'), d)

        self.assertEqual(r.status_code, 302)
        g = Participant.objects.last()
        self.assertEqual("/participants/{}/".format(g.id), r.url)


class TestParticipantCreateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        get_user_model().objects.create_user(**cls.dict)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-create'), d)

        self.assertEqual(r.status_code, 302)
        g = Participant.objects.last()
        self.assertEqual("/participants/{}/".format(g.id), r.url)


class TestParticipantCreateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'henri.buyse@gmail.com'
        }
        get_user_model().objects.create_superuser(**cls.dict)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-create'), d)

        self.assertEqual(r.status_code, 302)
        g = Participant.objects.last()
        self.assertEqual("/participants/{}/".format(g.id), r.url)
