# Generated by Django 4.1.7 on 2023-04-03 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_bookreview_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
