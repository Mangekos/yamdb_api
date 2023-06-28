import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import (Category, Genre, GenreTitle, Title, Comment,
                            Review, CustomUser)


DICT = {
    Category: 'category.csv',
    Genre: 'category.csv',
    GenreTitle: 'genry_title.csv',
    Title: 'titles.csv',
    Comment: 'comments.csv',
    Review: 'review.csv',
    CustomUser: 'users.csv'
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
