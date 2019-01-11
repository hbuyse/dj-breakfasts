#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from breakfasts.models import (
    Breakfast
)


class TestBreakfastListViewAsAnonymous(TestCase):
    """Tests ListView for Post."""

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_Breakfast(self):
        """Tests."""
        Breakfast.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )

        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_Breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Breakfast.objects.create(
                name='Watteau',
                address='37 rue Lequesne',
                city='Nogent-Sur-Marne',
                zip_code=94130,
                phone='0100000000',
                surface=123,
                capacity=456
            )

        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


class TestBreakfastListViewAsLogged(TestCase):
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
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_Breakfast(self):
        """Tests."""
        Breakfast.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_Breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Breakfast.objects.create(
                name='Watteau',
                address='37 rue Lequesne',
                city='Nogent-Sur-Marne',
                zip_code=94130,
                phone='0100000000',
                surface=123,
                capacity=456
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


class TestBreakfastListViewAsStaff(TestCase):
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
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_Breakfast(self):
        """Tests."""
        Breakfast.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_Breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Breakfast.objects.create(
                name='Watteau',
                address='37 rue Lequesne',
                city='Nogent-Sur-Marne',
                zip_code=94130,
                phone='0100000000',
                surface=123,
                capacity=456
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)


class TestBreakfastListViewAsSuperuser(TestCase):
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
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 0)

    def tests_list_view_one_Breakfast(self):
        """Tests."""
        Breakfast.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 1)

    def tests_list_view_multiple_Breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Breakfast.objects.create(
                name='Watteau',
                address='37 rue Lequesne',
                city='Nogent-Sur-Marne',
                zip_code=94130,
                phone='0100000000',
                surface=123,
                capacity=456
            )

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['breakfast_list']), 10)
