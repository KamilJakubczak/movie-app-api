from django.urls import path, include

from movie_api import views

app_name = 'api'



urlpatterns = [
    path('movies/', views.MovieApiView.as_view(), name='movies'),
    path('movies/<int:pk>/', views.MovieApiView.as_view()),
    path('comments/', views.CommentList.as_view(), name='comment'),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('top/', views.Top.as_view(), name='top'),
]
