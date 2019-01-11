#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from gymnasiums.models import (
    Gymnasium
)


class TestGymnasiumCreateViewAsAnonymous(TestCase):
    """Tests."""

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('gymnasiums:create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        r = self.client.post(reverse('gymnasiums:create'), d)

        self.assertEqual(r.status_code, 403)


class TestGymnasiumCreateViewAsLogged(TestCase):
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

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('gymnasiums:create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('gymnasiums:create'), d)

        self.assertEqual(r.status_code, 403)


class TestGymnasiumCreateViewAsStaff(TestCase):
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

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('gymnasiums:create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('gymnasiums:create'), d)

        self.assertEqual(r.status_code, 302)
        g = Gymnasium.objects.last()
        self.assertEqual("/{}".format(g.id), r.url)


class TestGymnasiumCreateViewAsSuperuser(TestCase):
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

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('gymnasiums:create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('gymnasiums:create'), d)

        self.assertEqual(r.status_code, 302)
        g = Gymnasium.objects.last()
        self.assertEqual("/{}".format(g.id), r.url)
