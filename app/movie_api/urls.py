from django.urls import path

from movie_api import views

app_name = 'api'

urlpatterns = [
    path('movies/', views.MovieApiView.as_view(), name='movies'),
]
