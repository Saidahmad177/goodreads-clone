from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from book.models import Book, BookReview


def landing_page(request):
    return render(request, 'landing_page.html')


def home_page(request):
    book = Book.objects.all().order_by('-created_time')
    book_review = BookReview.objects.all().order_by('-created_time')

    page_size = request.GET.get('page_size', 5)
    paginator = Paginator(book_review, page_size)
    page_num = request.GET.get('page', 1)
    pagination = paginator.get_page(page_num)

    # for i in book_review:
    #     print(i, '-----------------')

    context = {
        'latest_books': book[:10],
        'books': pagination,
        'range': range(5),
    }
    return render(request, 'home.html', context)


class SearchView(View):
    def get(self, request):
        books = Book.objects.all()
        search = request.GET.get('q', '')
        search_result = False
        count = None

        if search:
            search_result = books.filter(
                Q(name__icontains=search) |
                Q(isbn__icontains=search) |
                Q(bookauthor__author_id__first_name__icontains=search) |
                Q(bookauthor__author_id__last_name__icontains=search)
            )

            count = search_result.count()

        context = {
            'search_result': search_result,
            'result_count': count,
            'search': search,
        }

        return render(request, 'search.html', context)
