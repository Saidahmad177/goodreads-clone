from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from book.models import Author


class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all().order_by('-id')

        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(authors, page_size)
        page_num = request.GET.get('page')
        pagination = paginator.get_page(page_num)

        context = {
            'authors': pagination,
        }

        return render(request, 'author/author_list.html', context)


class AuthorDetailView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        context = {
            'author': author
        }

        return render(request, 'author/author-detail.html', context)
