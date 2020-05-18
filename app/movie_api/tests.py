from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from movie_api import models
from movie_api.models import Comment, Movie
from movie_api.serializers import CommentSerializer


MOVIE_URL = reverse('api:movies')
COMMENT_URL = reverse('api:comments')
COMMENT_SINGLE_URL = reverse('api:comment', args=[2])
TOP_URL = reverse('api:top')


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
            Writer="Dan O'Bannon (ett (story by)",
            Actors="Tom Skerritt, Sigourrry Dean Stanton",
            Plot="After a spaly begun.",
            Language="English",
            Country="UK, USA",
            Awards="Won 1 Oscar. Another 16 wins & 21 nominations.",
            Poster="https://m.media-amazon.",
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
            Metascore="89",
            imdbRating="8.4",
            imdbVotes="755,624",
            imdbID="tt0078748",
            Type="movie",
            DVD="N/A",
            BoxOffice="N/A",
            Production="N/A",
            Website="N/A",
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

    def test_create_movie_duplication(self):
        """Test of adding duplicated movie to db"""
        payload = {'title': 'Alien'}

        self.client.post(MOVIE_URL, payload)
        self.client.post(MOVIE_URL, payload)

        movie = Movie.objects.all()

        self.assertEqual(movie.count(), 1)


class CommentTests(TestCase):
    """
    Testcases for top view
    """
    def setUp(self):
        self.client = APIClient()

    def test_add_comment_successfully(self):
        """
        Check for adding comment
        """

        movie = MovieTests.mock_movie(self)
        Comment.objects.create(
            movie=movie,
            comment='test'
        )

        res = self.client.get(COMMENT_URL)
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_prevent_adding_blank_comment(self):
        """
        Check if adding blank comment is impossible
        """

        res = self.client.post(COMMENT_URL, {
            'movie': '5',
            'comment': ''
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_adding_comment_to_not_existing_movie(self):
        """
        Check if adding blank comment is impossible
        for non existing movie
        """

        res = self.client.post(COMMENT_URL, {
            'movie': '99',
            'comment': 'test'
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comment_for_existing_movie(self):
        """
        Check getting comments for existing movie
        """
        movie = MovieTests.mock_movie(self)
        Comment.objects.create(
            movie=movie,
            comment='test'
        )
        res = self.client.get(COMMENT_SINGLE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_comment_for_none_existing_movie(self):
        """
        Check getting comments for none existing movie
        """

        res = self.client.get(COMMENT_SINGLE_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class Top(TestCase):
    """
    Testcases for top view
    """
    def setUp(self):
        self.client = APIClient()

    def test_incorrect_date_format(self):
        """
        Checks for date validation
        """
        res = self.client.get(TOP_URL, {
            'date_from': '2020:05:05',
            'date_to': '2020-28-06'
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_if_to_grater_than_from(self):
        """
        Tescase checking if data range is valid
        """

        res = self.client.get(TOP_URL, {
            'date_from': '2020-05-02',
            'date_to': '2020-05-02'
        })

        res2 = self.client.get(TOP_URL, {
            'date_from': '2020-05-03',
            'date_to': '2020-05-02'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_for_missing_params(self):
        """
        Tescase if params are provided
        """

        res = self.client.get(TOP_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
