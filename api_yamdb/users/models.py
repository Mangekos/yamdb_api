from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from .validators import validate_name


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, role='', bio='', password=None):

        if not email:
            raise ValueError('Укажите email, пожалуйста!')
        if not username:
            raise ValueError('Укажите ваш username, пожулуйста!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            bio=bio,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, username, password, role='admin', bio=''
    ):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.role = role
        user.bio = bio
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class UserRole:

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Почта',
    )
    username = models.CharField(
        unique=True,
        validators=[validate_name],
        max_length=150,
        verbose_name='Имя пользователя'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Акстивный'
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Суперпользователь'
    )

    ROLE_CHOICES = (
        (UserRole.USER, 'Аутентифицированный пользователь'),
        (UserRole.MODERATOR, 'Модератор'),
        (UserRole.ADMIN, 'Администратор')
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default='user',
        max_length=64,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def is_user(self):

        return self.role == UserRole.USER

    @property
    def is_admin_or_superuser(self):

        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_admin_or_moderator(self):

        return (self.role in (UserRole.ADMIN, UserRole.MODERATOR)
                or self.is_superuser)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
