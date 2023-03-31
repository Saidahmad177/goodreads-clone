from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from book.models import Book


def home_page(request):
    return render(request, 'home.html')


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
