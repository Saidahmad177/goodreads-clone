from django.contrib import admin
from book.models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'description', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'bio')


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book_id', 'author_id')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('book_id', 'user', 'comment', 'stars')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
