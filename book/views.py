from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import View
from .models import Book


class BooksListView(View):
    def get(self, request):
        books_data = Book.objects.all().order_by('id')
        search = request.GET.get('q', '')
        if search:
            books_data = books_data.filter(name__icontains=search)

        page_size = request.GET.get('page_size', 6)
        paginator = Paginator(books_data, page_size)
        page_num = request.GET.get('page')
        pagenation = paginator.get_page(page_num)

        context = {
            'books': pagenation,
            'search_value': search
        }
        return render(request, 'books/book_list.html', context)


class DetailView(View):
    def get(self, request, slug):

        book_data = Book.objects.get(slug=slug)
        reviews = book_data.bookreview_set.all()
        author_book = book_data.bookauthor_set.all()

        context = {
            'book_detail': book_data,
            'reviews': reviews,
            'book_author': author_book,
        }

        return render(request, 'books/detail.html', context)

