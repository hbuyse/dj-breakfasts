#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Standard library
from datetime import date, timedelta

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings, tag
from django.urls import reverse

# Current django project
from breakfasts.models import Breakfast, Participant


@tag('breakfast', 'view', 'alternate', 'anonymous')
@override_settings(LOGIN_URL="/toto/")
class TestBreakfastAlternateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        for i in range(0, 3):
            Breakfast.objects.create(date=date.today() + timedelta(weeks=i), participant=cls.participant)

    def test_get(self):
        """Tests."""
        response = self.client.get(reverse('breakfasts:alternate'))

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)

    def test_no_data_post(self):
        """Tests."""
        d = {}
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)

    def test_empty_post(self):
        """Tests."""
        d = {
            "breakfast_list": []
        }
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)

    def test_too_little_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1]
        }
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)

    def test_too_much_item_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2, 3]
        }
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)

    def test_correct_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2]
        }
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertRedirects(response, "/toto/?next=/alternate/", fetch_redirect_response=False)


@tag('breakfast', 'view', 'alternate', 'logged')
class TestBreakfastAlternateViewAsLogged(TestCase):
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
        cls.participant = Participant.objects.create()
        for i in range(0, 3):
            Breakfast.objects.create(date=date.today() + timedelta(weeks=i), participant=cls.participant)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(response.status_code, 200)

    def test_no_data_post(self):
        """Tests."""
        d = {}
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_empty_post(self):
        """Tests."""
        d = {
            "breakfast_list": []
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_too_little_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        form = response.get("form")

        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_too_much_item_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2, 3]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_correct_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("breakfasts:next"))


@tag('breakfast', 'view', 'alternate', 'staff')
class TestBreakfastAlternateViewAsStaff(TestCase):
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
        cls.participant = Participant.objects.create()
        for i in range(0, 3):
            Breakfast.objects.create(date=date.today() + timedelta(weeks=i), participant=cls.participant)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(response.status_code, 200)

    def test_no_data_post(self):
        """Tests."""
        d = {}
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_empty_post(self):
        """Tests."""
        d = {
            "breakfast_list": []
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_too_little_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        form = response.get("form")

        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_too_much_item_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2, 3]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_correct_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("breakfasts:next"))


@tag('breakfast', 'view', 'alternate', 'superuser')
class TestBreakfastAlternateViewAsSuperuser(TestCase):
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
        cls.participant = Participant.objects.create()
        for i in range(0, 3):
            Breakfast.objects.create(date=date.today() + timedelta(weeks=i), participant=cls.participant)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.get(reverse('breakfasts:alternate'))

        self.assertEqual(response.status_code, 200)

    def test_no_data_post(self):
        """Tests."""
        d = {}
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_empty_post(self):
        """Tests."""
        d = {
            "breakfast_list": []
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "This field is required.")

    def test_too_little_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        form = response.get("form")

        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_too_much_item_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2, 3]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'breakfast_list', "You have to select two breakfast dates to alternate.")

    def test_correct_post(self):
        """Tests."""
        d = {
            "breakfast_list": [1, 2]
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))        
        response = self.client.post(reverse('breakfasts:alternate'), d)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("breakfasts:next"))
