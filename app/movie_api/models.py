from django.db import models


class Movie(models.Model):
    """Model for movie objects"""

    Title = models.CharField(max_length=255)
    Year = models.IntegerField()
    Rated = models.CharField(max_length=255)
    Released = models.CharField(max_length=255)
    Runtime = models.CharField(max_length=255)
    Genre = models.CharField(max_length=255)
    Director = models.CharField(max_length=255)
    Writer = models.CharField(max_length=255)
    Actors = models.CharField(max_length=255)
    Plot = models.TextField()
    Language = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    Awards = models.CharField(max_length=255)
    Poster = models.CharField(max_length=500)
    Ratings = models.CharField(max_length=500)
    Metascore = models.IntegerField()
    imdbRating = models.DecimalField(max_digits=3, decimal_places=1)
    imdbVotes = models.CharField(max_length=255)
    imdbID = models.CharField(max_length=255)
    Type = models.CharField(max_length=255)
    DVD = models.CharField(max_length=255)
    BoxOffice = models.CharField(max_length=255)
    Production = models.CharField(max_length=255)
    Website = models.CharField(max_length=255)
    Response = models.CharField(max_length=255)
