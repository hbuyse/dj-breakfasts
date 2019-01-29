#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from breakfasts.models import Participant


class TestParticipantDetailViewAsAnonymous(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-detail', kwargs={'pk': self.participant.id}))
        self.assertEqual(r.status_code, 200)


class TestParticipantDetailViewAsLogged(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-detail', kwargs={'pk': self.participant.id}))
        self.assertEqual(r.status_code, 200)


class TestParticipantDetailViewAsStaff(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-detail', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)


class TestParticipantDetailViewAsSuperuser(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-detail', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)
