from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=256, help_text='Заполнить имя жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True, help_text='Поле с уникальным значением')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256, help_text='Заполнить имя категории')
    slug = models.SlugField(
        max_length=50, unique=True, help_text='Поле с уникальным значением')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        help_text='Заполнить название произведения')
    year = models.IntegerField(
        help_text='Заполнить год создания')
    description = models.TextField(
        help_text='Заполнить описание к произведению')
    genre = models.ManyToManyField(
        Genre, related_name="titles",
        blank=True, help_text='Выбрать один или несколько жанров')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        blank=True, null=True, help_text='Выбрать категорию')

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(help_text='Напишите отзыв')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ], default=1, help_text='Оцените произведение от 1 до 10')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author_id'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(help_text='Напишите комментарий к отзыву')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
