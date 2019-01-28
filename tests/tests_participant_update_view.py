#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from breakfasts.models import Participant


class TestParticipantUpdateViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.participant_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        self.participant = Participant.objects.create(**self.participant_data)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/{}/update/'.format(self.participant.id))

    def test_post(self):
        """Tests."""
        self.participant_data['name'] = 'Watteau2'

        r = self.client.post(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}), self.participant_data)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/accounts/login/?next=/participants/{}/update/'.format(self.participant.id))


class TestParticipantUpdateViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**self.dict)

        self.participant_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        self.participant = Participant.objects.create(**self.participant_data)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.participant_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}), self.participant_data)

        self.assertEqual(r.status_code, 302)
        self.assertEqual("/participants/{}/".format(self.participant.id), r.url)


class TestParticipantUpdateViewAsStaff(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        get_user_model().objects.create_user(**self.dict)

        self.participant_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        self.participant = Participant.objects.create(**self.participant_data)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.participant_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}), self.participant_data)

        self.assertEqual(r.status_code, 302)
        self.assertEqual("/participants/{}/".format(self.participant.id), r.url)


class TestParticipantUpdateViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'henri.buyse@gmail.com'
        }
        get_user_model().objects.create_superuser(**self.dict)

        self.participant_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com'
        }
        self.participant = Participant.objects.create(**self.participant_data)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.participant_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:participant-update', kwargs={'pk': self.participant.id}), self.participant_data)

        self.assertEqual(r.status_code, 302)
        self.assertEqual("/participants/{}/".format(self.participant.id), r.url)
