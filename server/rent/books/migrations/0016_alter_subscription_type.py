# Generated by Django 4.1.1 on 2022-10-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_alter_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.IntegerField(choices=[(0, 'Нет подписки'), (1, 'Стандарт'), (2, 'Плюс'), (3, 'Премиум')], verbose_name='Тип'),
        ),
    ]
