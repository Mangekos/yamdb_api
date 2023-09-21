import random

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser


def get_tokens_for_user(user):
    """Функция токена для пользвателя."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


def send_confirmation_code_to_email(username):
    """Функция для отправки кода."""
    user = get_object_or_404(CustomUser, username=username)
    confirmation_code = int(
        ''.join([str(random.randrange(settings.MIN_SCORE_VALUE,
                                      settings.MAX_SCORE_VALUE))
                 for _ in range(settings.CONFIRMATION_CODE_LENGTH)])
    )
    user.confirmation_code = confirmation_code
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {user.confirmation_code}',
        settings.ADMIN_EMAIL,
        (user.email,),
        fail_silently=False,
    )
    user.save()
