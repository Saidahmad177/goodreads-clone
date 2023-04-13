from rest_framework import serializers

from book.models import Book, BookReview
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'slug', 'description', 'isbn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class BookReviewSerializer(serializers.ModelSerializer):
    book_name = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    book_name_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'stars', 'comment', 'user', 'book_name', 'book_name_id', 'user_id')
