import requests
import os


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from django.core import serializers as srz
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
        
        if pk == None:
            movies = Movie.objects.all()
            print(movies.count())
            serializer = self.movie_serializer_class(movies, many=True)
        else:
            movies = Movie.objects.get(id=pk)
            print(movies.count())
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
                # movie_serializer.is_valid()
                # print(movie_serializer.errors)
                if movie_serializer.is_valid():
                    print('valid')
                    # movie_serializer.save()
                    saved_movie = Movie.objects.create(**movie_data.json())
                    # print(saved_movie)

                    # data = srz.serialize('json', saved_movie)
                    # print(data)
                return Response({'details': movie_data.json()})
                    # return Response({'data':saved_movie})

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
    """Get all comments and add new one"""
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
    """Detailed view for comment objects"""

    def get_object(self, pk):
        try:
            return Comment.objects.all().filter(movie__id=pk)
        except Comment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, type=None):
        """Retreive comments from db"""

        comment = self.get_object(pk)
        serializer = serializers.CommentSerializer(comment, many=True)
        return Response(serializer.data)