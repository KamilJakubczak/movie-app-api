from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    """Serializer for movie objects"""

    title = serializers.CharField(max_length=255)
