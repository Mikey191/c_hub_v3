from django import template
from movies.models import Tag, Genre, Director, Actor, Movie

register = template.Library()


@register.inclusion_tag('movies/tags_list.html')
def show_tags():
    tags = Tag.objects.all()
    return {'tags': tags}


@register.inclusion_tag('movies/genres_list.html')
def show_genres():
    genres = Genre.objects.all()
    return {'genres': genres}


@register.inclusion_tag('movies/directors_list.html')
def show_directors(limit=10):
    directors = Director.objects.all()[:limit]
    return {'directors': directors}


@register.inclusion_tag('movies/actors_list.html')
def show_actors(limit=10):
    actors = Actor.objects.all()[:limit]
    return {'actors': actors}


@register.inclusion_tag('movies/tags_list.html')
def show_tags_small():
    # альтернатива: можно вернуть только несколько тегов
    tags = Tag.objects.all()[:10]
    return {'tags': tags}


@register.inclusion_tag('movies/recent_movies_list.html')
def show_recent_movies(limit=5):
    movies = Movie.objects.filter(is_published=True).order_by('-created_at')[:limit].prefetch_related('tags')
    return {'movies': movies}
