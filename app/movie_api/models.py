from django.db import models


class Movie(models.Model):
    """Model for movie objects"""

    Title = models.CharField(max_length=255)
    Year = models.CharField(max_length=255)
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
    Metascore = models.CharField(max_length=255)
    imdbRating = models.CharField(max_length=255)
    imdbVotes = models.CharField(max_length=255)
    imdbID = models.CharField(max_length=255)
    Type = models.CharField(max_length=255)
    DVD = models.CharField(max_length=255)
    BoxOffice = models.CharField(max_length=255)
    Production = models.CharField(max_length=255)
    Website = models.CharField(max_length=255)
    Response = models.CharField(max_length=255)

    def __str__(self):
        return self.Title


class Comment(models.Model):
    """Models for comment objects"""
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    added_on = models.DateField()
