# Generated by Django 4.1.1 on 2022-10-03 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_alter_subscription_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.IntegerField(choices=[(1, 'Стандарт'), (2, 'Плюс'), (3, 'Премиум')], verbose_name='Тип'),
        ),
    ]