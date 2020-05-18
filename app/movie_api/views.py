import requests
import os
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from movie_api import serializers
from movie_api.serializers import CommentSerializer
from movie_api.models import Movie, Comment

EXTERNAL_API_LINK = 'http://www.omdbapi.com'


class MovieApiView(APIView):
    """Movie API view"""

    serializers_class = serializers.TitleSerialzier
    movie_serializer_class = serializers.MovieSerializer

    def get(self, request, pk=None, type=None):
        """Return items"""

        if pk is None:
            movies = Movie.objects.all()
            serializer = self.movie_serializer_class(movies, many=True)
        else:
            movies = Movie.objects.get(id=pk)
            serializer = self.movie_serializer_class(movies, many=False)

        return Response(serializer.data)

    def post(self, request):
        """Create request for movie details and sate the result to db"""

        serializer = self.serializers_class(data=request.data)
        # Ping external API
        if serializer.is_valid():
            title = serializer.validated_data.get('title')

            payload = {
                'i': os.environ.get('I'),
                'apikey': os.environ.get('API_KEY'),
                't': title,
            }

            movie_data = requests.post(
                EXTERNAL_API_LINK,
                params=payload
            )
            # Return 400 if movie has not been found
            if 'Error' in movie_data.json().keys():
                return Response(
                    {'error': movie_data.json()['Error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            movie_serializer = self.movie_serializer_class(
                data=movie_data.json()
            )
            # Check if movie already exist in database
            try:
                exists = Movie.objects.get(
                    Title=movie_data.json()['Title']
                )
            except:
                exists = None
            if not exists:
                if movie_serializer.is_valid():
                    movie_serializer.save()

                if bool(movie_serializer.errors):
                    return Response({
                        'error': 'error movie not saved in db'
                    }, status=status.HTTP_400_BAD_REQUEST)
                return Response(movie_serializer.data)
            else:
                serializer = self.movie_serializer_class(
                    exists,
                    many=False
                )
                return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentList(APIView):
    """
    Get all comments and add new one
    """
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CommentDetail(APIView):
    """
    Detailed view for comment objects
    """

    def get_object(self, pk):
        try:
            return Comment.objects.all().filter(movie__id=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, type=None):
        """
        Get comments from db for provided movie id
        """

        comment = self.get_object(pk)
        serializer = serializers.CommentSerializer(comment, many=True)
        return Response(serializer.data)


class Ranking:
    """
    Simple object of movie id, count of related object
    and ranking place
    """

    def __init__(self, movie_id, total_comments):
        self.movie_id = movie_id
        self.total_comments = total_comments

    def set_ranking(self, rank):
        self.rank = rank


class Top(APIView):
    """
    Returns top movies for secific data range
    """

    def valid_date(self, date_str):
        """ Validate the date format"""
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def compare_dates(self, from_date, to_date):
        """Check if to date is grater then from"""

        from_data = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        if from_data > to_date:
            return False
        else:
            return True

    def get(self, request):
        """
        Returns the top movies list based on number of comments
        for specified date range
        - from yyyy-mm-dd
        - to yyy-mm-dd
        """

        # Get request data
        since = self.request.query_params.get('date_from')
        to = self.request.query_params.get('date_to')
        if since is None or to is None:
            return Response(
                {'error': '''no dates provided'''},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Date range validation
        if not self.valid_date(since) \
           or not self.valid_date(to) \
           or not self.compare_dates(since, to):

            return Response({
                'error': '''dates are  in invalid format, use yyyy-mm-dd'''},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all movie objects from db
        all_movies = Movie.objects.all()

        # Get list of movies along wuth comment number
        response = []
        for movie in all_movies:
            total_comments = Comment.objects.all().filter(
                movie__id=movie.id
            ).filter(
                added_on__gte=since
            ).filter(
                added_on__lte=to
            ).count()
            list_item = Ranking(movie.id, total_comments)
            response.append(list_item)
        response = sorted(
            response,
            key=lambda total: total.total_comments,
            reverse=True
        )

        # Set rank
        for item in range(len(response)):
            prev = response[item-1]
            cur = response[item]
            try:
                if response[item-1].rank \
                and (prev.total_comments == cur.total_comments):
                    cur.set_ranking(prev.rank)
                else:
                    cur.set_ranking(prev.rank+1)
            except:
                cur.set_ranking(1)

        # Set objects to be JSONable
        res = []
        for i in response:
            res.append(i.__dict__)

        return Response(res)
