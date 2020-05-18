from rest_framework import serializers

from movie_api.models import Movie, Comment


class TitleSerialzier(serializers.Serializer):
    """Serializer for movie objects"""
    title = serializers.CharField(max_length=255)


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie objects"""
    Ratings = serializers.JSONField()

    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment objects"""

    class Meta:
        model = Comment
        fields = ('id', 'movie', 'comment', 'added_on')
        read_only_fields = ('id', 'added_on')