# Generated by Django 4.2.3 on 2023-09-19 09:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('add', '0005_advertisement_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_adv', to=settings.AUTH_USER_MODEL),
        ),
    ]
