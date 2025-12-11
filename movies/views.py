from django.shortcuts import render, get_object_or_404
from .models import Movie, Tag, Genre, Director, Actor


def index(request):
    """
    Список всех опубликованных фильмов.
    """
    title = "Список фильмов"
    films = Movie.objects.filter(is_published=True).select_related().prefetch_related('tags', 'genres', 'directors', 'actors')
    context = {
        'title': title,
        'films': films,
    }
    return render(request, 'movies/index.html', context)


def movie_detail(request, pk):
    """
    Детальная страница фильма.
    """
    film = get_object_or_404(Movie, pk=pk, is_published=True)
    title = f"Фильм: {film.title}"
    return render(request, 'movies/movie_detail.html', {'title': title, 'film': film})


def films_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    films = Movie.objects.filter(tags__slug=slug, is_published=True).distinct().prefetch_related('tags', 'genres', 'directors', 'actors')
    title = f"Фильмы по тегу: {tag.name}"
    return render(request, 'movies/index.html', {'title': title, 'films': films})


def films_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    films = Movie.objects.filter(genres__slug=slug, is_published=True).distinct().prefetch_related('tags', 'genres', 'directors', 'actors')
    title = f"Фильмы жанра: {genre.name}"
    return render(request, 'movies/index.html', {'title': title, 'films': films})


def films_by_director(request, pk):
    director = get_object_or_404(Director, pk=pk)
    films = Movie.objects.filter(directors__id=pk, is_published=True).distinct().prefetch_related('tags', 'genres', 'directors', 'actors')
    title = f"Фильмы режиссёра: {director.name}"
    return render(request, 'movies/index.html', {'title': title, 'films': films})


def films_by_actor(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    films = Movie.objects.filter(actors__id=pk, is_published=True).distinct().prefetch_related('tags', 'genres', 'directors', 'actors')
    title = f"Фильмы с актёром: {actor.name}"
    return render(request, 'movies/index.html', {'title': title, 'films': films})
