from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ForeignKey(
        Genre,
        related_name='titles',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)

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
        CustomUser,
        models.CASCADE
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    # class Meta:
    #     orderind = ('pub_date',)

    def __str__(self):
        return {self.text}


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
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
