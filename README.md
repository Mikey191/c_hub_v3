# Django: с_hub

## Структура проекта

```
project_root/
├─ manage.py
├─ core/
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ movies/
│  ├─ migrations/
│  │   └─ **init**.py
│  ├─ management/commands/seed.py
│  ├─ templatetags/
│  │   ├─ **init**.py
│  │   └─ movie_tags.py
│  ├─ templates/
│  │   ├─ base.html
│  │   └─ movies/
│  │      ├─ index.html
│  │      ├─ movie_detail.html
│  │      ├─ tags_list.html
│  │      ├─ genres_list.html
│  │      ├─ directors_list.html
│  │      ├─ actors_list.html
│  │      └─ recent_movies_list.html
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py
│  └─ admin.py
├─ requirements.txt
└─ .gitignore
```

---

## Запуск проекта

### 1) Клонирование репозитория

```bash
git clone <URL_репозитория>
```

### 2) Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows
```

### 3) Установка библиотек

```bash
pip install -r requirements.txt
```

### 4) Создание и Применение миграций

```bash
python manage.py makemigrations
```

и

```bash
python manage.py migrate
```

### 5) Запуск локального сервера

```bash
python manage.py runserver
```

---

## Генерация данных (SEED)

В проект встроена кастомная команда:

```bash
python manage.py seed
```

По умолчанию создаёт:

- **теги (по умолчанию 10)**
- **жанры (по умолчанию 8)**
- **режиссёры (+ профили) (по умолчанию 10)**
- **актёры (+ профили) (по умолчанию 30)**
- **фильмы (по умолчанию 40)**

### Принудительное выполнение

По умолчанию команда **не перезаписывает существующие данные**.
Чтобы форсировать (перезаписать) данные используйте:

```bash
python manage.py seed --force
```

**Опции команды:**

```bash
python manage.py seed --force             # удалить ранее сгенерированные объекты и создать заново
python manage.py seed --movies 50         # задать количество фильмов
python manage.py seed --actors 60         # задать количество актёров
python manage.py seed --directors 15      # задать количество режиссёров
python manage.py seed --tags 20
python manage.py seed --genres 12
```

---

## Доступные URLs

- `http://127.0.0.1:8000/` — список всех опубликованных фильмов (index)
- `http://127.0.0.1:8000/movie/<pk>/` — детальная страница фильма
- `http://127.0.0.1:8000/tag/<slug>/` — фильмы по тегу
- `http://127.0.0.1:8000/genre/<slug>/` — фильмы по жанру
- `http://127.0.0.1:8000/director/<pk>/` — фильмы конкретного режиссёра
- `http://127.0.0.1:8000/actor/<pk>/` — фильмы с конкретным актёром

---
