from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DirectorProfile(models.Model):
    director = models.OneToOneField(
        Director,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Профиль режиссёра: {self.director.name}"


class Actor(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ActorProfile(models.Model):
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Профиль актёра: {self.actor.name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='movies', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='movies')
    genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
    directors = models.ManyToManyField(Director, blank=True, related_name='movies')
    actors = models.ManyToManyField(Actor, blank=True, related_name='movies')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', 'title')

    def __str__(self):
        return self.title
