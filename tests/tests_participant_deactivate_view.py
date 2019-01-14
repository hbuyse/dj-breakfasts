#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from breakfasts.models import (
    Participant
)


class TestVcnAccountDeleteViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/{}/deactivate/'.format(self.participant.id))

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/{}/deactivate/'.format(self.participant.id))


class TestVcnAccountDeleteViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)
        self.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))
        self.assertEqual(r.status_code, 302)


class TestVcnAccountDeleteViewAsStaff(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        self.staff = get_user_model().objects.create_user(**self.dict)
        self.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)


class TestVcnAccountDeleteViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.dict)
        self.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)
