from django.test import TestCase
from django.urls import reverse

from friend.models import Friends
from users.models import CustomUser


class FriendsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru',
        )
        self.user.set_password('testpassword')
        self.user.save()

        self.user2 = CustomUser.objects.create(
            username='testuser2',
            first_name='testname2',
            last_name='testname2',
            email='test@mail.ru',
        )
        self.user2.set_password('testpassword')
        self.user2.save()

        self.user3 = CustomUser.objects.create(
            username='testuser3',
            first_name='testname3',
            last_name='testname3',
            email='test@mail.ru',
        )
        self.user3.set_password('testpassword')
        self.user3.save()

        self.follower = Friends.objects.create(
            requester=self.user2,
            recipient=self.user,
            accepted=True,
        )
        self.following = Friends.objects.create(
            requester=self.user,
            recipient=self.user2,
            accepted=True,
        )

    def test_friends_list(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('friends:friends'))

        followers = Friends.objects.filter(recipient=self.user)
        following = Friends.objects.filter(requester=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(following.count(), 1)
        self.assertEqual(followers.count(), 1)

        for follower in followers:
            self.assertContains(response, follower.requester)

        for follow in following:
            self.assertContains(response, follow.recipient)

        self.assertNotContains(response, self.user3)

