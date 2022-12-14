# Generated by Django 4.1.1 on 2022-09-27 14:08

import books.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0010_book_subscription_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='books.genre', verbose_name='Жанры'),
        ),
        migrations.AlterField(
            model_name='book',
            name='subscription_type',
            field=models.CharField(choices=[('standart', 'Стандарт'), ('plus', 'Плюс'), ('premium', 'Премиум')], max_length=8, verbose_name='Тип подписки'),
        ),
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(related_name='books', to='books.tag', verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='book',
            name='upload',
            field=models.FileField(default='', upload_to=books.utils.author_directory_path, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='like',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='books.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='duration',
            field=models.IntegerField(choices=[(3, '3 месяца'), (6, '6 месяцев'), (12, 'год')], verbose_name='Длительность подписки в месяцах'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.CharField(choices=[('standart', 'Стандарт'), ('plus', 'Плюс'), ('premium', 'Премиум')], max_length=8, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
