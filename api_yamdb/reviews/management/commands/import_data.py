import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser

DICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    GenreTitle: 'genre_title.csv',
    Title: 'titles.csv',
    Comment: 'comments.csv',
    Review: 'review.csv',
    CustomUser: 'users.csv'
}


def category_import():
    if Category.objects.exists():
        print('Данные для Category уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/category.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )


def genre_import():
    if Genre.objects.exists():
        print('Данные для Genre уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/genre.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )


def genre_title_import():
    if GenreTitle.objects.exists():
        print('Данные для GenreTitle уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/genre_title.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )


def title_import():
    if Title.objects.exists():
        print('Данные для Title уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/titles.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )


def comments_import():
    if Comment.objects.exists():
        print('Данные для Comment уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/comments.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=CustomUser.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )


def review_import():
    if Review.objects.exists():
        print('Данные для Review уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/review.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=CustomUser.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )


def users_import():
    if CustomUser.objects.exists():
        print('Данные для CustomUser уже загружены')
    else:
        with open(
            f'{settings.BASE_DIR}/static/data/users.csv',
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                CustomUser.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )


class Command(BaseCommand):
    help = "Импортируем данные из CSV файлов в вашу модель"

    def handle(self, *args, **options):
        users_import()
        genre_import()
        category_import()
        title_import()
        genre_title_import()
        review_import()
        comments_import()
        self.stdout.write(self.style.SUCCESS('Данные импортированы успешно'))
