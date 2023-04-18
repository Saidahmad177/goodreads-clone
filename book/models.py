from django.db import models
from django.utils import timezone

from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    book_image = models.ImageField(upload_to='books/', default='default_book.jpg')
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    social_network = models.CharField(max_length=100)
    bio = models.TextField()
    member_since = models.CharField(max_length=50)
    author_img = models.ImageField(upload_to='authors/', default='default_pic.jpg')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book_id} | {self.author_id}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}- {self.book_name}"
