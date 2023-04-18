from django.test import TestCase
from django.urls import reverse

from book.models import Author


class AuthorListTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Victor',
            last_name='Lavella',
            social_network='test@mail.ru',
            bio='fantastic author',
            member_since='March 2019',

        )
        self.author2 = Author.objects.create(
            first_name='Rachel',
            last_name='Heng',
            social_network='test2@mail.ru',
            bio='fine very good',
            member_since='june 2020',

        )
        self.author3 = Author.objects.create(
            first_name='Alka',
            last_name='Joshi',
            social_network='test3@mail.ru',
            bio='good very good',
            member_since='September 2013',

        )
        self.author4 = Author.objects.create(
            first_name='aji',
            last_name='buji',
            social_network='test4@mail.ru',
            bio='great is great',
            member_since='January 2022',

        )

    def test_authors_list(self):
        # response = self.client.get(reverse('author:author_list'))
        url = reverse('author:author_list') + '?page_size=2'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author4.full_name())
        self.assertContains(response, self.author3.full_name())
        # print(response.content.decode())
        self.assertNotContains(response, self.author2.full_name())
        self.assertNotContains(response, self.author.full_name())

        response = self.client.get(reverse('author:author_list') + '?page=2&page_size=2')
        for author in [self.author2, self.author]:
            self.assertContains(response, author.full_name())

        self.assertNotContains(response, self.author3.full_name())
        self.assertNotContains(response, self.author4.full_name())

    def test_author_detail(self):
        response = self.client.get(reverse('author:author-detail-page', kwargs={'id': self.author.id}))

        self.assertContains(response, 'Victor Lavella')
        self.assertContains(response, 'March 2019')
        self.assertContains(response, 'fantastic author')
        self.assertContains(response, 'test@mail.ru')



