from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    bio = models.TextField('Биография', max_length=500, blank=True)
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0]
    )
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        default=random.randint(100000, 999999)
    )

    def __str__(self):
        return f'{self.username}, статус: {self.role}'
