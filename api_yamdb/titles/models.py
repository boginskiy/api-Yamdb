from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name="titles", blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    def __str__(self):
        return self.name
