from datetime import date

from django.db import models

from .constants import SUBSCRIPTION_TYPES, SUBSCRIPTION_DURATIONS
from .utils import author_directory_path, add_months_to_date


class Book(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    upload = models.FileField(
        upload_to=author_directory_path,
        default='',
        verbose_name='Файл',
    )
    author = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор',
    )
    tags = models.ManyToManyField(
        to='books.Tag',
        related_name='books',
        verbose_name='Тэги',
    )
    genres = models.ManyToManyField(
        to='books.Genre',
        related_name='books',
        verbose_name='Жанры',
    )
    subscription_type = models.IntegerField(
        choices=SUBSCRIPTION_TYPES,
        verbose_name='Тип подписки',
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    type = models.IntegerField(
        choices=SUBSCRIPTION_TYPES,
        verbose_name='Тип',
    )
    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Пользователь',
    )
    duration = models.IntegerField(
        verbose_name='Длительность подписки в месяцах',
        choices=SUBSCRIPTION_DURATIONS,
    )
    start_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата начала подписки',
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Подписка на книги'
        verbose_name_plural = 'Подписки на книги'

    def __str__(self):
        return f'{self.user.username} -- {self.type} ({self.duration})'

    @property
    def days_to_end(self):
        return (add_months_to_date(self.start_date, self.duration) - date.today()).days


class Tag(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title


class Like(models.Model):
    book = models.ForeignKey(
        to='books.Book',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Книга',
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пользователь',
    )
    liked_time = models.DateTimeField(
        auto_now_add=True,
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user.username} --> {self.book.title} (liked)'
