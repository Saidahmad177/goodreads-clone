from django.test import TestCase
from django.urls import reverse

from book.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_home_page(self):
        book = Book.objects.create(name='name', slug='slug', description='description', isbn='111111')

        user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru',
        )
        user.set_password('testpassword')
        user.save()
        # self.client.login(username='testuser', password='testpassword')

        review1 = BookReview.objects.create(book_name=book, user=user, stars=2, comment='Very good book')
        review2 = BookReview.objects.create(book_name=book, user=user, stars=3, comment='this is Useful')
        review3 = BookReview.objects.create(book_name=book, user=user, stars=4, comment='it great')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)

        self.assertNotContains(response, review1.comment)

        response = self.client.get(reverse('home_page') + '?page=2&page_size=2')
        self.assertContains(response, review1.comment)
        self.assertNotContains(response, review2.comment)
        self.assertNotContains(response, review3.comment)


