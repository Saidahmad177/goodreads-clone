from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book


class BooksTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru'

        )
        user.set_password('testpassword')
        user.save()

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
        self.client.login(username='testuser', password='testpassword')

        book = Book.objects.create(name='title1', slug='test-slug', description='description1', isbn='isbn1')

        response = self.client.get(reverse('book:detail_view', kwargs={'slug': book.slug}))

        self.assertContains(response, book.name)
        self.assertContains(response, book.description)
        # self.assertContains(response, book.isbn)

    def test_review_book(self):
        user = CustomUser.objects.create(
            username='testuser2',
            first_name='testname',
            last_name='testname',
            email='test2@mail.ru'

        )
        user.set_password('testpassword')
        user.save()
        self.client.login(username='testuser2', password='testpassword')

        book = Book.objects.create(name='title1', slug='test-slug', description='description1', isbn='isbn1')

        self.client.post(reverse('book:detail_view', kwargs={'slug': book.slug}), data={
            'stars': 5,
            'comment': 'some comment'
        })
        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars, 5)
        self.assertEqual(book_reviews[0].comment, 'some comment')
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book_name, book)

    def test_error_book(self):
        user = CustomUser.objects.create(
            username='testuser3',
            first_name='testname',
            last_name='testname',
            email='test3@mail.ru'

        )
        user.set_password('testpassword')
        user.save()
        self.client.login(username='testuser3', password='testpassword')

        book = Book.objects.create(name='title1', slug='test-slug', description='description1', isbn='isbn1')

        self.client.post(reverse('book:detail_view', kwargs={'slug': book.slug}), data={
            'stars': 3,
            'comment': 'some comment'
        })
        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertNotEqual(book_reviews[0].stars, 7)
        self.assertEqual(book_reviews[0].comment, 'some comment')
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book_name, book)

    def test_search_case(self):
        book1 = Book.objects.create(name='first', slug='first', description='description1', isbn='11111')
        book2 = Book.objects.create(name='second', slug='second', description='description2', isbn='22222')
        book3 = Book.objects.create(name='third', slug='third', description='description3', isbn='33333')

        response = self.client.get(reverse('search') + '?q=first')
        self.assertContains(response, book1.name)
        self.assertNotContains(response, book2.name)
        self.assertNotContains(response, book3.name)

        response = self.client.get(reverse('search') + '?q=second')
        self.assertContains(response, book2.name)
        self.assertNotContains(response, book1.name)
        self.assertNotContains(response, book3.name)

        response = self.client.get(reverse('search') + '?q=third')
        self.assertContains(response, book3.name)
        self.assertNotContains(response, book1.name)
        self.assertNotContains(response, book2.name)


