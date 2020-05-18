from django.db import models


class Movie(models.Model):
    """Model for movie objects"""

    title = models.CharField(max_length=255)
