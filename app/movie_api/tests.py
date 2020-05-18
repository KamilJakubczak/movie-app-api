from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from movie_api import models
from movie_api import serializers


MOVIE_URL = reverse('api:movies')
# MOVIE_URL_FIRST = reverse('api:movies:1')


class MovieTests(TestCase):
    """Testcases for movie objects"""

    def setUp(self):
        self.client = APIClient()

    def mock_movie(self):
        """Return mock movie for testing pourpose"""


        return models.Movie.objects.create(
            Title="Alien",
            Year="1979",
            Rated="R",
            Released="22 Jun 1979",
            Runtime="117 min",
            Genre="Horror, Sci-Fi",
            Director="Ridley Scott",
            Writer="Dan O'Bannon (screenplay by), Dan O'Bannon (story by), Ronald Shusett (story by)",
            Actors="Tom Skerritt, Sigourney Weaver, Veronica Cartwright, Harry Dean Stanton",
            Plot="After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun.",
            Language="English",
            Country="UK, USA",
            Awards="Won 1 Oscar. Another 16 wins & 21 nominations.",
            Poster="https://m.media-amazon.com/images/M/MV5BMmQ2MmU3NzktZjAxOC00ZDZhLTk4YzEtMDMyMzcxY2IwMDAyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            Ratings=[
                {
                    "Source": "Internet Movie Database",
                    "Value": "8.4/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "98%"
                },
                {
                    "Source": "Metacritic",
                    "Value": "89/100"
                }
            ],
            Metascore= "89",
            imdbRating= "8.4",
            imdbVotes= "755,624",
            imdbID= "tt0078748",
            Type= "movie",
            DVD= "N/A",
            BoxOffice= "N/A",
            Production= "N/A",
            Website= "N/A",
            Response="True"
        )

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

    def test_add_the_same_movie(self):
        """Test checkig if adding the same movie is not allowed"""
        
        movie = self.mock_movie()

        payload = {'title': 'Alien'}
        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


