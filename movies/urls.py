from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:pk>/', views.movie_detail, name='detail'),
    path('tag/<slug:slug>/', views.films_by_tag, name='by_tag'),
    path('genre/<slug:slug>/', views.films_by_genre, name='by_genre'),
    path('director/<int:pk>/', views.films_by_director, name='by_director'),
    path('actor/<int:pk>/', views.films_by_actor, name='by_actor'),
]
