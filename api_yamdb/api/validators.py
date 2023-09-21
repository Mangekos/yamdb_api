import re
from datetime import date

from rest_framework.serializers import ValidationError

REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')


def title_year_validator(value):
    """Проверяем валидность года выпуска."""
    year_now = date.today().year
    if 0 <= value <= year_now:
        return value
    raise ValidationError(
        'Год выпуска не может быть больше текущего!')


def validate_slug(slug):
    """Функция проверки корректности имени пользователя."""
    if not REGEX_FOR_USERNAME.fullmatch(slug):
        raise ValidationError(
            'Можно использовать только буквы, цифры и "@.+-_".')
