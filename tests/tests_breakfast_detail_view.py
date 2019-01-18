#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from gymnasiums.models import (
    Gymnasium
)


class TestVcnAccountDetailViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('gymnasiums:detail', kwargs={'pk': self.gymnasium.id}))
        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsLogged(TestCase):
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

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('gymnasiums:detail', kwargs={'pk': self.gymnasium.id}))
        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsStaff(TestCase):
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

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('gymnasiums:detail', kwargs={'pk': self.gymnasium.id}))

        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsSuperuser(TestCase):
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

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('gymnasiums:detail', kwargs={'pk': self.gymnasium.id}))

        self.assertEqual(r.status_code, 200)
