# Generated by Django 4.1.7 on 2023-04-14 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_book_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_img',
            field=models.ImageField(default='default_pic.jpg', upload_to='authors/'),
        ),
    ]