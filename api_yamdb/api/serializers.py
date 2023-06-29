
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

from .validators import title_year_validator


class ReviewSerializer(serializers.ModelSerializer):
    """Обработка отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    def validate(self, data):
        request = self.context['request']
        view = self.context['view']
        author = request.user
        title_id = view.kwargs.get('title_id')

        if (Review.objects.filter(
            author=author, title_id=title_id).exists()
                and request.method != 'PATCH'):
            raise serializers.ValidationError(
                'Нельзя оставлять отзыв несколько раз'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Обработка комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""
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

    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True)
    year = serializers.IntegerField(validators=[title_year_validator])

    class Meta:
        fields = ('id', 'name',
                  'year', 'description',
                  'genre', 'category', 'rating')
        model = Title


class TitleCreateSerializer(TitleSerializer):
    """Сериализатор для создания произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')
        model = Title
