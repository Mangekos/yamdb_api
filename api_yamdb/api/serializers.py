
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import validate_email
from django.db.models import Avg
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    """Обработка отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Обработка комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )


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
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        read_only_fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    def get_rating(self, title):
        rating = Review.objects.filter(
            title=title).aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return None

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',
                  'rating')
        model = Title
