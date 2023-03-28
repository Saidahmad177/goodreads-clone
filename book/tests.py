from django.test import TestCase
from django.urls import reverse

from .models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("book:books_list"))

        self.assertContains(response, 'No books data.')

    def test_books_list(self):
        Book.objects.create(name='title1', description='description1', isbn='isbn1')
        Book.objects.create(name='title2', description='description2', isbn='isbn2')
        Book.objects.create(name='title3', description='description3', isbn='isbn3')

        response = self.client.get(reverse('book:books_list'))
        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.name)

    def test_detail_page(self):
        book = Book.objects.create(name='title1', description='description1', isbn='isbn1')

        response = self.client.get(reverse('book:detail_view', kwargs={'id': book.id}))

        self.assertContains(response, book.name)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)
