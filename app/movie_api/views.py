import requests
import os


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers as srz

from movie_api import serializers
from movie_api.models import Movie

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
