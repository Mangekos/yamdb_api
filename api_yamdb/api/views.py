from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, pagination, permissions, response, status,
                            views, viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
from users.utils import get_tokens_for_user

from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdminOrReadOnly, OnlyAdminPermission,
                          ReadOnlyOrAuthorOrAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleSerializer)
from .utils import send_confirmation_code_to_email


class CustomUserViewSet(viewsets.ModelViewSet):
    """View-set для эндпоинта users."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [OnlyAdminPermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        """Обработка метода PATCH."""
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        serializer = CustomUserSerializer(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def signup(request):
    """Функция проверки входа."""
    username = request.data.get('username')
    if CustomUser.objects.filter(username=username).exists():
        user = get_object_or_404(CustomUser, username=username)
        serializer = SignUpSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['email'] != user.email:
            return response.Response(
                'Почта указана неверно!', status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(raise_exception=True)
        send_confirmation_code_to_email(username)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['username'] != 'me':
        serializer.save()
        send_confirmation_code_to_email(username)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response(
        (
            'Использование имени пользователя '
            '-me- запрещено!'
        ),
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersMeApiView(views.APIView):
    """Отдельно описываем поведение для users/me."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Получаем себя при обращении на users/me."""
        serializer = CustomUserSerializer(self.request.user)
        return response.Response(serializer.data)

    def patch(self, request):
        """Изменяем свои поля."""
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request},
                                          data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def get_token(request):
    """Функция для токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(CustomUser, username=request.data['username'])
    confirmation_code = serializer.data.get('confirmation_code')
    if confirmation_code == str(user.confirmation_code):
        return response.Response(
            get_tokens_for_user(user),
            status=status.HTTP_200_OK)
    return response.Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [ReadOnlyOrAuthorOrAdmin]
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
    permission_classes = [ReadOnlyOrAuthorOrAdmin]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = get_object_or_404(Review, id=review_id)
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
