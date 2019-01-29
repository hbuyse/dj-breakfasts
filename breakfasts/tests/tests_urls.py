#!/usr/bin/env python
# coding=utf-8

"""Tests for `breakfasts` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse


class TestUrlsBreakfast(TestCase):
    """Tests the urls for the breakfasts."""

    def test_breakfast_index_url(self):
        """Test the index URL."""
        url = reverse('breakfasts:index')
        self.assertEqual(url, '/')

    def test_breakfast_next_url(self):
        """Test the URL of the listing of the next breakfasts."""
        url = reverse('breakfasts:next')
        self.assertEqual(url, '/next/')

    def test_breakfast_past_url(self):
        """Test the URL of the listing of the past breakfasts."""
        url = reverse('breakfasts:past')
        self.assertEqual(url, '/past/')

    def test_breakfast_create_url(self):
        """Test the URL of that allows the creation of a breakfast."""
        url = reverse('breakfasts:create')
        self.assertEqual(url, '/create/')

    def test_breakfast_detail_url(self):
        """Test the URL that gives the details of a breakfast."""
        url = reverse('breakfasts:detail', kwargs={'pk': 1})
        self.assertEqual(url, '/1/')

    def test_breakfast_update_url(self):
        """Test the URL of the listing of breakfasts."""
        url = reverse('breakfasts:update', kwargs={'pk': 1})
        self.assertEqual(url, "/1/update/")

    def test_breakfast_delete_url(self):
        """Test the URL of the listing of breakfasts."""
        url = reverse('breakfasts:delete', kwargs={'pk': 1})
        self.assertEqual(url, "/1/delete/")


class TestUrlsParticipant(TestCase):
    """Tests the urls for the participants."""

    def test_participant_list_url(self):
        """Test the participants list URL."""
        url = reverse('breakfasts:participant-list')
        self.assertEqual(url, '/participants/')

    def test_participant_create_url(self):
        """Test the participant creation URL."""
        url = reverse('breakfasts:participant-create')
        self.assertEqual(url, '/participants/create/')

    def test_participant_detail_url(self):
        """Test the participant detail URL."""
        url = reverse('breakfasts:participant-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/participants/1/')

    def test_participant_update_url(self):
        """Test the participant modification URL."""
        url = reverse('breakfasts:participant-update', kwargs={'pk': 1})
        self.assertEqual(url, '/participants/1/update/')

    def test_participant_deactivate_url(self):
        """Test the participant deactivation URL."""
        url = reverse('breakfasts:participant-deactivate', kwargs={'pk': 1})
        self.assertEqual(url, '/participants/1/deactivate/')
