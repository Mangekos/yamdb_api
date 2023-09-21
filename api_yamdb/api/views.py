from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, pagination, viewsets)

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdminOrReadOnly, ReadOnlyOrAuthorOrAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleCreateSerializer,
                          TitleSerializer)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = pagination.PageNumberPagination
    ordering_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('category', 'genre', 'year', 'name')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (ReadOnlyOrAuthorOrAdmin,)
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = get_object_or_404(Title, id=title_id)
        return new_queryset.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (ReadOnlyOrAuthorOrAdmin,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title__id = self.kwargs.get('title_id')
        new_queryset = get_object_or_404(
            Review, id=review_id, title__id=title__id
        )
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        title__id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title__id=title__id)
        serializer.save(author=self.request.user, review=review)
