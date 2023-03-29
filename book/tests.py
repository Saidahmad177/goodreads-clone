from django.test import TestCase
from django.urls import reverse

from .models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("book:books_list"))

        self.assertContains(response, 'No books data.')

    def test_books_list(self):
        book1 = Book.objects.create(name='title1', slug='test-slug', description='description1', isbn='isbn1')
        book2 = Book.objects.create(name='title2', slug='test-slug', description='description2', isbn='isbn2')
        book3 = Book.objects.create(name='title3', slug='test-slug', description='description3', isbn='isbn3')

        response = self.client.get(reverse('book:books_list') + '?page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.name)
        self.assertNotContains(response, book3.name)

        response = self.client.get(reverse('book:books_list') + '?page=2&page_size=2')
        self.assertContains(response, book3.name)

    def test_detail_page(self):
        book = Book.objects.create(name='title1', slug='test-slug', description='description1', isbn='isbn1')

        response = self.client.get(reverse('book:detail_view', kwargs={'slug': book.slug}))

        self.assertContains(response, book.name)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)

    def test_search_case(self):
        book1 = Book.objects.create(name='sea', slug='test-slug', description='description1', isbn='isbn1')
        book2 = Book.objects.create(name='lone', slug='test-slug', description='description2', isbn='isbn2')
        book3 = Book.objects.create(name='grid', slug='test-slug', description='description3', isbn='isbn3')

        response = self.client.get(reverse('book:books_list') + '?q=sea')
        self.assertContains(response, book1.name)
        self.assertNotContains(response, book2)
        self.assertNotContains(response, book3)

        response = self.client.get(reverse('book:books_list') + '?q=lone')
        self.assertContains(response, book2.name)
        self.assertNotContains(response, book1)
        self.assertNotContains(response, book3)

        response = self.client.get(reverse('book:books_list') + '?q=grid')
        self.assertContains(response, book3.name)
        self.assertNotContains(response, book1)
        self.assertNotContains(response, book2)

