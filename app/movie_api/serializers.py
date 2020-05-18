from rest_framework import serializers

from movie_api.models import Movie


class TitleSerialzier(serializers.Serializer):
    """Serializer for movie objects"""
    title = serializers.CharField(max_length=255)


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie objects"""
    Ratings = serializers.JSONField()

    class Meta:
        model = Movie
        fields = '__all__'
