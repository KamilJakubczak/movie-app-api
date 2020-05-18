from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


MOVIE_URL = reverse('api:movies')


class MovieTests(TestCase):
    """Testcases for movie objects"""

    def setUp(self):
        self.client = APIClient()

    def test_create_movie_successful(self):
        """Test creating a new movie seccessfully"""
        payload = {'title': 'Alien'}
        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_movie_unsuccessful(self):
        """Test creating a new movie unseccessfully"""
        payload = {'title': ''}
        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
