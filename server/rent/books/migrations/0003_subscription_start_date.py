# Generated by Django 4.1.1 on 2022-09-23 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='start_date',
            field=models.DateField(auto_created=True, default=None, verbose_name='Дата начала подписки'),
            preserve_default=False,
        ),
    ]
