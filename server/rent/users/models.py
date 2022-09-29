from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name='Приватный аккаунт',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username} ({self.email})'


class Follow(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='follows',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор',
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписки на пользователей'

    def __str__(self) -> str:
        return f'{self.user.username} --> {self.author.username}'
