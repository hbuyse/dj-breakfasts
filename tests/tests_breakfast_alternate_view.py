#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from breakfasts.models import Breakfast, Participant


class TestBreakfastCreateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast_1 = Breakfast.objects.last()
        cls.breakfast_2 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )
        cls.breakfast_3 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(r.status_code, 302)

    def test_empty_post(self):
        """Tests."""
        d = {
            "breakfast_list": []
        }
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 200)

    def test_too_little_post(self):
        """Tests."""
        d = {
            "breakfast_list": ["1"]
        }
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)

    def test_too_much_item_post(self):
        """Tests."""
        d = {
            "breakfast_list": ["1", "2", "3"]
        }
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)

    def test_correct_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2]
        }
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)


class TestBreakfastCreateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast_1 = Breakfast.objects.last()
        cls.breakfast_2 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )
        cls.breakfast_3 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(r.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 2)


class TestBreakfastCreateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            "is_staff": True
        }
        get_user_model().objects.create_user(**cls.dict)
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast_1 = Breakfast.objects.last()
        cls.breakfast_2 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )
        cls.breakfast_3 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(r.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 2)


class TestBreakfastCreateViewAsSuperuser(TestCase):
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
        cls.participant = Participant.objects.create(
            first_name="first_name",
            last_name="last_name",
            email="email@email.com"
        )
        cls.breakfast_1 = Breakfast.objects.last()
        cls.breakfast_2 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )
        cls.breakfast_3 = Breakfast.objects.create(
            date=Breakfast.objects.last().date + timedelta(weeks=1),
            participant=cls.participant
        )

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'participant': self.participant.id,
            'date': date.today() + timedelta(weeks=1)
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(r.status_code, 302)
        b = Breakfast.objects.last()
        self.assertEqual(r.url, reverse('breakfasts:detail', args=(b.id,)))
        self.assertEqual(len(Breakfast.objects.all()), 2)
