from django.core.exceptions import ValidationError


def validate_name(value):
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" в качестве username')
    return value
