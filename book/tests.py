from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book, Author, BookAuthor, BookReview


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
        book1 = Book.objects.create(name='title1', slug='title1', description='description1', isbn='111111')
        book2 = Book.objects.create(name='Shoe Dog', slug='shoe-dog', description='description2', isbn='222222')
        book3 = Book.objects.create(name='Sea Change', slug='sea-change', description='description3', isbn='333333')

        response = self.client.get(reverse('book:books_list') + '?page_size=2')

        for book in [book3, book2]:
            self.assertContains(response, book.name)
        self.assertNotContains(response, book1.name)

        response = self.client.get(reverse('book:books_list') + '?page=2&page_size=2')
        self.assertContains(response, book1.name)

    def test_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        author = Author.objects.create(first_name='John', last_name='Doe')
        author2 = Author.objects.create(first_name='Charl', last_name='Karl')
        book = Book.objects.create(name='Sea Change',
                                   slug='sea-change',
                                   isbn='978363636212',
                                   description='It is very good book'
                                   )
        BookAuthor.objects.create(book_id=book, author_id=author)
        response = self.client.get(reverse('book:detail_view', kwargs={'slug': book.slug}))
        self.assertContains(response, book.name)
        self.assertContains(response, book.description)
        self.assertNotContains(response, author2.first_name)
        self.assertNotContains(response, author2.last_name)

        for i in book.bookauthor_set.all():
            self.assertContains(response, i.author_id.full_name())

    def test_review_book(self):
        user = CustomUser.objects.create(
            username='testuser2',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru'

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


class ReviewEditTestCase(TestCase):
    def test_edit_review(self):
        user = CustomUser.objects.create(
            username='testuser',
            email='test@mail.ru',
        )
        user.set_password('testpassword')
        user.save()

        book = Book.objects.create(
            name='Sea change',
            slug='sea-change',
            description='sea is a good',
            isbn='111111'
        )
        review = BookReview.objects.create(
            book_name=book,
            user=user,
            stars=4,
            comment='some comment'
        )
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('book:edit-review', kwargs={'slug': book.slug, 'review_id': review.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('book:edit-review', kwargs={'slug': book.slug, 'review_id': review.id}),
                                    data={'stars': 1, 'comment': 'this is very good book'})
        self.assertRedirects(response, reverse('book:detail_view', kwargs={'slug': book.slug}))
        self.assertEqual(response.status_code, 302)

        review.refresh_from_db()
        self.assertEqual(review.stars, 1)
        self.assertEqual(review.comment, 'this is very good book')

