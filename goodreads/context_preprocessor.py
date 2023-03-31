from book.models import Book
from django.views.generic import View


def context_function(reqeuest):
    book_data = Book.objects.all().order_by('id')
    search = reqeuest.GET.get('q', '')

    if search:
        book_data = Book.objects.filter(name__icontains=search)

    context = {
        'global_book_data': book_data,
        'search_value': search
    }
    return context

