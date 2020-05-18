import requests
import os


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from movie_api import serializers

EXTERNAL_API_LINK = 'http://www.omdbapi.com'


class MovieApiView(APIView):
    """Movie API view"""

    serializers_class = serializers.MovieSerializer

    def get(self, request, type=None):
        """Return items"""
        return Response({'list': 'items'})

    def post(self, request):
        """Create request for movie details and sate the result to db"""
        serializer = self.serializers_class(data=request.data)

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

            if 'Error' in movie_data.json().keys():
                return Response(
                    {'error': movie_data.json()['Error']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({'details': movie_data.json()})

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
