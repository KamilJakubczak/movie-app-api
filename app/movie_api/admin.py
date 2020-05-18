from django.contrib import admin
from movie_api import models
# Register your models here.
admin.site.register(models.Movie)
admin.site.register(models.Comment)