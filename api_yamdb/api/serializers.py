
from django.forms import ValidationError
from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth.validators import ASCIIUsernameValidator
from reviews.models import Category, Genre, Title
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = CustomUser

    def validate(self, data):
        request = self.context['request']
        if (request.method == 'PATCH'
                and request.data.get('role')
                and request.user.is_user):
            data['role'] = 'user'
        return data


class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Не верное поле email')
        return value

    def validate_username(self, value):

        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username'
            )

        try:
            ASCIIUsernameValidator(value)
        except ValidationError:
            raise serializers.ValidationError('Не корректные данные username')
        return value

    def validate(self, data):

        if CustomUser.objects.filter(username=data['username']).exists():
            if (
                CustomUser.objects.get(username=data['username']).email
            ) == data['email']:
                raise serializers.ValidationError('Некорректный email')
        return data


class GetTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

