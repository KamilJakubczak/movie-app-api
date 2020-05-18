from django.db import models


class Movie(models.Model):
    """Model for movie objects"""

    Title = models.CharField(max_length=255, blank=True)
    Year = models.CharField(max_length=255, blank=True)
    Rated = models.CharField(max_length=255, blank=True)
    Released = models.CharField(max_length=255, blank=True)
    Runtime = models.CharField(max_length=255, blank=True)
    Genre = models.CharField(max_length=255, blank=True)
    Director = models.CharField(max_length=255, blank=True)
    Writer = models.CharField(max_length=255, blank=True)
    Actors = models.CharField(max_length=255, blank=True)
    Plot = models.TextField(blank=True)
    Language = models.CharField(max_length=255, blank=True)
    Country = models.CharField(max_length=255, blank=True)
    Awards = models.CharField(max_length=255, blank=True)
    Poster = models.CharField(max_length=500, blank=True)
    Ratings = models.CharField(max_length=500, blank=True)
    Metascore = models.CharField(max_length=255, blank=True)
    imdbRating = models.CharField(max_length=255, blank=True)
    imdbVotes = models.CharField(max_length=255, blank=True)
    imdbID = models.CharField(max_length=255, blank=True)
    Type = models.CharField(max_length=255, blank=True)
    DVD = models.CharField(max_length=255, blank=True)
    BoxOffice = models.CharField(max_length=255, blank=True)
    Production = models.CharField(max_length=255, blank=True)
    Website = models.CharField(max_length=255, blank=True)
    Response = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.Title


class Comment(models.Model):
    """Models for comment objects"""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    added_on = models.DateField()
