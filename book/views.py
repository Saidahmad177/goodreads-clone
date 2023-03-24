from django.shortcuts import render
from django.views.generic import View
from .models import Book


class BooksListView(View):
    def get(self, request):
        books_data = Book.objects.all()
        context = {
            'books': books_data
        }

        return render(request, 'books/book_list.html', context)


class DetailView(View):
    def get(self, request, id):
        book_data = Book.objects.get(id=id)

        return render(request, 'books/detail.html', {'book_detail': book_data})

