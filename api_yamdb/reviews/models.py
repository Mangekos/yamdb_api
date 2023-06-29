from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint
from api_yamdb.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name = 'Произведения'

    def __str__(self):
        return {self.name}


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre}, {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        models.CASCADE
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_rewiev'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
