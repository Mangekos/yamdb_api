from api.permissions import OnlyAdminPermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, pagination, permissions, response, status,
                            views, viewsets)
from rest_framework.decorators import api_view, permission_classes
from users.models import CustomUser
from users.utils import get_tokens_for_user

from .serializers import (CustomUserSerializer, GetTokenSerializer,
                          SignUpSerializer)
from .utils import send_confirmation_code_to_email


class CustomUserViewSet(viewsets.ModelViewSet):
    """View-set для эндпоинта users."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (OnlyAdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def signup(request):
    """Функция проверки входа."""
    username = request.data.get('username')
    email = request.data.get('email')
    if CustomUser.objects.filter(username=username, email=email).exists():
        user = get_object_or_404(CustomUser, username=username)
        serializer = SignUpSerializer(
            user, data=request.data, partial=True
        )
    else:
        serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_confirmation_code_to_email(username)
    return response.Response(serializer.data, status=status.HTTP_200_OK)


class UsersMeApiView(views.APIView):
    """Отдельно описываем поведение для users/me."""
    permission_classes = (permissions.IsAuthenticated,)

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
    message = {'confirmation_code': 'Код подтверждения не верен'}
    return response.Response(
        message,
        status=status.HTTP_400_BAD_REQUEST)
