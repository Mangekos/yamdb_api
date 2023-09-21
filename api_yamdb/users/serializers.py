from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = CustomUser

    def validate(self, data):
        """Поле роль обычному юзеру менять запрещено."""
        request = self.context['request']
        if (request.method == 'PATCH'
                and request.data.get('role')
                and request.user.is_user):
            data['role'] = 'user'
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта регистрации пользователей."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)
