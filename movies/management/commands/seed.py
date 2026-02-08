from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction
from faker import Faker
import random
from datetime import datetime
import os
from django.conf import settings
from django.core.files import File

from movies.models import (
    Category,
    Tag,
    Genre,
    Director,
    DirectorProfile,
    Actor,
    ActorProfile,
    Movie,
)

fake = Faker()

SEED_IMAGE_PATH = os.path.join(
    settings.BASE_DIR,
    "img_for_seed",
    "avatar.jpg"
)

class Command(BaseCommand):
    help = "Seed DB: create tags, genres, directors (+profiles), actors (+profiles) and movies."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete existing seeded objects before creating new ones",
        )
        parser.add_argument(
            "--tags", type=int, default=10, help="Number of tags to create"
        )
        parser.add_argument(
            "--genres", type=int, default=8, help="Number of genres to create"
        )
        parser.add_argument(
            "--directors", type=int, default=10, help="Number of directors to create"
        )
        parser.add_argument(
            "--actors", type=int, default=30, help="Number of actors to create"
        )
        parser.add_argument(
            "--movies", type=int, default=40, help="Number of movies to create"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get("force", False)
        n_tags = options.get("tags")
        n_genres = options.get("genres")
        n_directors = options.get("directors")
        n_actors = options.get("actors")
        n_movies = options.get("movies")

        if force:
            self.stdout.write(
                "Удаление существующих объектов movies/... (будьте внимательны)..."
            )
            Movie.objects.all().delete()
            DirectorProfile.objects.all().delete()
            Director.objects.all().delete()
            ActorProfile.objects.all().delete()
            Actor.objects.all().delete()
            Tag.objects.all().delete()
            Genre.objects.all().delete()

        # Tags
        self.stdout.write("Создаём теги...")
        tag_names = set()
        while len(tag_names) < n_tags:
            name = fake.unique.word().capitalize()
            tag_names.add(name)

        tags = []
        for name in tag_names:
            slug = slugify(name)
            tag, _ = Tag.objects.get_or_create(slug=slug, defaults={"name": name})
            tags.append(tag)
        self.stdout.write(f"Теги: {len(tags)}")

        # Genres
        self.stdout.write("Создаём жанры...")
        genre_names = set()
        while len(genre_names) < n_genres:
            name = fake.unique.word().capitalize()
            genre_names.add(name)

        genres = []
        for name in genre_names:
            slug = slugify(name)
            genre, _ = Genre.objects.get_or_create(slug=slug, defaults={"name": name})
            genres.append(genre)
        self.stdout.write(f"Жанры: {len(genres)}")

        # Directors + profiles
        self.stdout.write("Создаём режиссёров и профили...")
        directors = []
        for _ in range(n_directors):
            name = fake.unique.name()
            slug = slugify(name)
            director, _ = Director.objects.get_or_create(
                slug=slug, defaults={"name": name}
            )
            DirectorProfile.objects.update_or_create(
                director=director,
                defaults={
                    "bio": fake.paragraph(nb_sentences=5),
                    "birthday": fake.date_of_birth(minimum_age=25, maximum_age=90),
                },
            )
            directors.append(director)
        self.stdout.write(f"Режиссёры: {len(directors)}")

        # Actors + profiles
        self.stdout.write("Создаём актёров и профили...")
        actors = []
        for _ in range(n_actors):
            name = fake.unique.name()
            slug = slugify(name)
            actor, _ = Actor.objects.get_or_create(slug=slug, defaults={"name": name})
            ActorProfile.objects.update_or_create(
                actor=actor,
                defaults={
                    "bio": fake.paragraph(nb_sentences=4),
                    "birthday": fake.date_of_birth(minimum_age=18, maximum_age=80),
                },
            )
            actors.append(actor)
        self.stdout.write(f"Актёры: {len(actors)}")
        
        # Categories
        self.stdout.write("Создаём категории...")
        category_names = ["0+", "4+", "6+", "12+", "16+", "18+"]

        categories = []
        for name in category_names:
            slug = slugify(name)
            category = Category.objects.create(name=name, slug=slug)
            categories.append(category)
        self.stdout.write(f"Категории: {len(categories)}")

        # Movies
        self.stdout.write("Создаём фильмы...")
        movies = []
        generated_titles = set()
        attempts = 0
        while len(generated_titles) < n_movies and attempts < n_movies * 10:
            attempts += 1
            t = fake.sentence(nb_words=3).rstrip(".")
            generated_titles.add(t)

        for title in list(generated_titles)[:n_movies]:
            description = fake.paragraph(nb_sentences=6)
            year = random.randint(1950, datetime.now().year)
            movie = Movie.objects.create(
                title=title,
                description=description,
                year=year,
                category=random.choice(categories),
                is_published=random.choice([True] * 9 + [False]),
            )

            # Добавляем постер ко всем фильмам
            if os.path.exists(SEED_IMAGE_PATH):
                with open(SEED_IMAGE_PATH, "rb") as img_file:
                    movie.poster.save(
                        "avatar.jpg",
                        File(img_file),
                        save=True
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Файл {SEED_IMAGE_PATH} не найден. Постер не добавлен."
                    )
                )

            # attach tags (0..4)
            if tags:
                k = random.randint(0, min(4, len(tags)))
                if k:
                    movie.tags.add(*random.sample(tags, k))

            # attach genres (1..2)
            if genres:
                k = random.randint(1, min(2, len(genres)))
                movie.genres.add(*random.sample(genres, k))

            # attach directors (1..2)
            if directors:
                k = random.randint(1, min(2, len(directors)))
                movie.directors.add(*random.sample(directors, k))

            # attach actors (2..6)
            if actors:
                k = random.randint(2, min(6, len(actors)))
                movie.actors.add(*random.sample(actors, k))

            movies.append(movie)

        self.stdout.write(self.style.SUCCESS(f"Фильмы: {len(movies)} созданы."))
        self.stdout.write(self.style.SUCCESS("Seeding finished."))
        self.stdout.write("Запустите: python manage.py runserver и проверьте сайт.")
