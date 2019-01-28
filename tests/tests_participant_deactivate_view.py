#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

# Current django project
from breakfasts.models import Participant


@override_settings(LOGIN_URL="/toto/")
class TestVcnAccountDeactivateViewAsAnonymous(TestCase):
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
        self.assertEqual(r.url, '/toto/?next=/participants/{id}/deactivate/'.format(id=self.participant.id))

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('breakfasts:participant-deactivate', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/toto/?next=/participants/{id}/deactivate/'.format(id=self.participant.id))
        participant = Participant.objects.get(id=self.participant.id)
        self.assertTrue(participant.is_active)


class TestVcnAccountDeactivateViewAsLogged(TestCase):
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
        self.assertEqual(r.url, reverse('breakfasts:participant-list'))
        participant = Participant.objects.get(id=self.participant.id)
        self.assertFalse(participant.is_active)


class TestVcnAccountDeactivateViewAsStaff(TestCase):
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
        self.assertEqual(r.url, reverse('breakfasts:participant-list'))
        participant = Participant.objects.get(id=self.participant.id)
        self.assertFalse(participant.is_active)


class TestVcnAccountDeactivateViewAsSuperuser(TestCase):
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
        self.assertEqual(r.url, reverse('breakfasts:participant-list'))
        participant = Participant.objects.get(id=self.participant.id)
        self.assertFalse(participant.is_active)
