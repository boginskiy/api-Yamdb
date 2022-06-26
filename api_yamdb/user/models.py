from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Manager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        user = self.model(username=username, email=email, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(username=username, email=email, )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    email = models.EmailField(unique=True)
    bio = models.TextField('Биография', max_length=500, blank=True)
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0]
    )
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        null=True
    )

    REQUIRED_FIELDS = ['email']

    objects = Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_follower')
        ]

    def __str__(self):
        return f'{self.username}, статус: {self.role}'
