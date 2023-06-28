
from rest_framework import mixins, viewsets, filters
from users.models import CustomUser
from rest_framework import permissions, status
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import (
    OnlyAdminPermissions
)
from .serializers import (
    CustomUserSerializer, SignUpSerializer, GetTokenSerializer
)
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title,
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer,
                    

class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [OnlyAdminPermissions]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username')
    lookup_field = 'username'


class SignUpUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()

    @staticmethod
    def send_confirmation_code(user, to_email):

        mail_subject = 'Email confirmation. YamDb'
        token = default_token_generator.make_token(user)
        message = (
            'Для завершения регистрации подтвердите Ваш email.'
            f'\nToken:{token}'
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                'Такой email уже используется.',
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        user, created = CustomUser.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
        to_email = serializer.validated_data['email']
        if created:
            user.is_active = False
            user.save()
            SignUpUserViewSet.send_confirmation_code(user, to_email)
            return Response(serializer.data, status.HTTP_200_OK)
        SignUpUserViewSet.send_confirmation_code(user, to_email)
        return Response(serializer.data, status.HTTP_200_OK)


class UsersMeApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = CustomUserSerializer(self.request.user)
        return Response(serializer.data)

    def patch(self, request):

        user = self.request.user
        serializer = CustomUserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        if not CustomUser.objects.filter(username=username).exists():
            return Response(
                'Пользователь не найден.', status=status.HTTP_404_NOT_FOUND
            )
        user = CustomUser.objects.get(username=username)
        if not default_token_generator.check_token(
                user, confirmation_code
        ):
            return Response(
                'Неверный e-mail.', status=status.HTTP_400_BAD_REQUEST
            )
        access_token = RefreshToken.for_user(user).access_token
        user.is_active = True
        user.save()
        data = {"token": str(access_token)}
        return Response(data, status=status.HTTP_200_OK)

        
class CreateDestroyListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    pass


class CategoryGenreViewSet(CreateDestroyListViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ('name',)
