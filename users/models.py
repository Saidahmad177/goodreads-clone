from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_img = models.ImageField(default='default_pic.jpg')
