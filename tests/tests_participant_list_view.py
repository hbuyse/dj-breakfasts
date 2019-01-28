#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from breakfasts.models import Participant


class TestParticipantListViewAsAnonymous(TestCase):
    """Tests ListView for Post."""

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 0)

    def tests_list_view_one_participant(self):
        """Tests."""
        Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 1)

    def tests_list_view_multiple_participants(self):
        """Tests."""
        for i in range(0, 10):
            Participant.objects.create(
                first_name="first_name",
                last_name="last_name",
                email="email@email.com"
            )

        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 10)


class TestParticipantListViewAsLogged(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 0)

    def tests_list_view_one_participant(self):
        """Tests."""
        Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 1)

    def tests_list_view_multiple_participants(self):
        """Tests."""
        for i in range(0, 10):
            Participant.objects.create(
                first_name="first_name",
                last_name="last_name",
                email="email@email.com"
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 10)


class TestParticipantListViewAsStaff(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 0)

    def tests_list_view_one_participant(self):
        """Tests."""
        Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 1)

    def tests_list_view_multiple_participants(self):
        """Tests."""
        for i in range(0, 10):
            Participant.objects.create(
                first_name="first_name",
                last_name="last_name",
                email="email@email.com"
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 10)


class TestParticipantListViewAsSuperuser(TestCase):
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
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 0)

    def tests_list_view_one_participant(self):
        """Tests."""
        Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 1)

    def tests_list_view_multiple_participants(self):
        """Tests."""
        for i in range(0, 10):
            Participant.objects.create(
                first_name="first_name",
                last_name="last_name",
                email="email@email.com"
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['participant_list']), 10)
