from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from book.models import BookReview, Book
from users.models import CustomUser


class BookReviewApiTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@mail.ru')
        self.user2 = CustomUser.objects.create(username='testuser2', email='test2@mail.ru')
        self.user.set_password('testpassword')
        self.user2.set_password('testpassword')
        self.user.save()
        self.user2.save()

        self.client.login(username='testuser', password='testpassword')

        self.book = Book.objects.create(
            name='book1',
            slug='slug',
            description='description',
            isbn='isbn'
        )
        self.review = BookReview.objects.create(book_name=self.book, user=self.user, stars=3, comment='some comment')
        self.review2 = BookReview.objects.create(book_name=self.book, user=self.user, stars=2, comment='good book')

    def test_review_api(self):
        response = self.client.get(reverse('api:book_review'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], self.review2.id)
        self.assertEqual(response.data['results'][0]['stars'], self.review2.stars)
        self.assertEqual(response.data['results'][0]['comment'], self.review2.comment)
        self.assertEqual(response.data['results'][1]['id'], self.review.id)
        self.assertEqual(response.data['results'][1]['stars'], self.review.stars)
        self.assertEqual(response.data['results'][1]['comment'], self.review.comment)

        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_review_detail_api(self):
        response = self.client.get(reverse('api:review_detail', kwargs={'id': self.review.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.review.id)
        self.assertEqual(response.data['stars'], self.review.stars)
        self.assertEqual(response.data['comment'], self.review.comment)
        self.assertEqual(response.data['book_name']['id'], self.book.id)
        self.assertEqual(response.data['book_name']['name'], self.book.name)
        self.assertEqual(response.data['book_name']['slug'], self.book.slug)
        self.assertEqual(response.data['book_name']['description'], self.book.description)
        self.assertEqual(response.data['book_name']['isbn'], self.book.isbn)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_review_create(self):
        response = self.client.post(reverse('api:book_review'),
                                    data={'comment': 'some comment',
                                          'stars': 3,
                                          'user_id': self.user.id,
                                          'book_name_id': self.book.id
                                          }
                                    )
        self.assertEqual(response.status_code, 201)
        book_review = self.book.bookreview_set.all()
        self.assertEqual(book_review[0].stars, 3),
        self.assertEqual(book_review[0].comment, 'some comment'),
        self.assertEqual(book_review[0].user_id, self.user.id),
        self.assertEqual(book_review[0].book_name_id, self.book.id)

    def test_review_detail_put(self):
        self.client.put(reverse('api:review_detail', kwargs={'id': self.review.id}),
                        data={
                            'comment': 'great',
                            'stars': 5,
                            'book_name_id': self.book.id,
                            'user_id': self.user.id
                        }
                        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.stars, 5)
        self.assertEqual(self.review.comment, 'great')

    def test_review_detail_patch(self):
        self.client.patch(reverse('api:review_detail', kwargs={'id': self.review.id}),
                          data={'comment': 'great'})

        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'great')

    def test_review_detail_delete(self):
        response = self.client.delete(reverse('api:review_detail', kwargs={'id': self.review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=self.review.id))
