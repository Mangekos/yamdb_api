from rest_framework import serializers
from reviews.models import Comment, Review, Title
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg


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


class TitleSerializer(serializers.ModelSerializer):
    """Обработка произведений."""
    rating = serializers.SerializerMethodField()

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
