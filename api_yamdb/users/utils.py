from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Функция токена для пользвателя."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }
