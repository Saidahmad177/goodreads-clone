from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import Book, BookReview
from .forms import BookReviewForm


class BooksListView(View):
    def get(self, request):
        books_data = Book.objects.all().order_by('-id')
        book_ratings = []

        for book in books_data:
            most_common_rating = BookReview.objects.filter(book_name=book, stars__range=[1, 5]).values('stars').annotate(
                stars_count=Count('stars')).order_by('-stars_count').first()
            if most_common_rating is not None:
                book_ratings.append((book, most_common_rating['stars'], most_common_rating['stars_count']))
            else:
                book_ratings.append((book, None, None))

        page_size = request.GET.get('page_size', 6)
        paginator = Paginator(book_ratings, page_size)
        page_num = request.GET.get('page')
        pagenation = paginator.get_page(page_num)

        context = {
            'books': pagenation,
            'book_ratings': book_ratings,
            'range': range(5),
        }
        return render(request, 'books/book_list.html', context)


class DetailView(LoginRequiredMixin, View):
    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        reviews = BookReview.objects.filter(book_name=book)
        author_book = book.bookauthor_set.all()
        review_count = reviews.count()
        context = {
            'book_detail': book,
            'reviews': reviews,
            'book_author': author_book,
            'range': range(5),
            'review_count': review_count,
        }

        return render(request, 'books/detail.html', context)

    def post(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
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
        return redirect(reverse('book:detail_view', kwargs={'slug': slug}))


class DeleteReview(View):
    def get(self, request, slug, review_id):
        book = get_object_or_404(Book, slug=slug)
        review = book.bookreview_set.get(id=review_id)
        review.delete()

        return redirect(reverse('book:detail_view', kwargs={'slug': slug}))


class EditReview(View):
    def get(self, request, slug, review_id):
        book = Book.objects.get(slug=slug)
        review = book.bookreview_set.get(id=review_id)
        context = {
            'review': review,
            'book': book,
            'range': range(5)

        }

        return render(request, 'books/review_edit.html', context)

    def post(self, request, slug, review_id):
        book = Book.objects.get(slug=slug)
        review = book.bookreview_set.get(id=review_id)
        form = BookReviewForm(instance=review, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('book:detail_view', kwargs={'slug': book.slug}))

        context = {
            'book': book,
            'review': review,
        }

        return render(request, 'books/review_edit.html', context)
