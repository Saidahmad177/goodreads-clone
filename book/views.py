from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import Book, BookReview
from .forms import BookReviewForm


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
        book = get_object_or_404(Book, slug=slug)
        reviews = BookReview.objects.filter(book_name=book)
        author_book = book.bookauthor_set.all()
        form = BookReviewForm()
        context = {
            'book_detail': book,
            'reviews': reviews,
            'form': form,
            'book_author': author_book,
            'range': range(5)
        }

        return render(request, 'books/detail.html', context)

    def post(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        author_book = book.bookauthor_set.all()
        form = BookReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['stars']
            comment = form.cleaned_data['comment']
            BookReview.objects.create(
                book_name=book,
                user=request.user,
                stars=rating,
                comment=comment
            )
        reviews = BookReview.objects.filter(book_name=book)
        context = {
            'book_detail': book,
            'reviews': reviews,
            'form': form,
            'book_author': author_book,
        }
        return redirect(reverse('book:detail_view', kwargs={'slug': slug}))



















