# Generated by Django 4.1.1 on 2022-10-06 07:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_alter_subscription_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='liked_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]