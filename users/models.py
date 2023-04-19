from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_img = models.ImageField(default='default_pic.jpg')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    user = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email
