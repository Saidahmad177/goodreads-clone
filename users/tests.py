from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class UserRegisterTest(TestCase):
    def test_user_is_created(self):
        self.client.post(
            reverse('users:signup'),
            data={
                'username': 'testuser',
                'first_name': 'testname',
                'last_name': 'testname',
                'email': 'test@mail.ru',
                'password': 'testpassword'
            }
        )

        user = CustomUser.objects.get(username='testuser')

        self.assertEqual(user.first_name, 'testname')
        self.assertEqual(user.last_name, 'testname')
        self.assertEqual(user.email, 'test@mail.ru')
        # self.assertEqual(user.password, 'testpassword')
        self.assertTrue(user.check_password('testpassword'))

    def test_user_required(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'first_name': 'testname',
                'email': 'test@mail.ru',
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'username': 'testuser',
                'first_name': 'testname',
                'last_name': 'testname',
                'email': 'test',
                'password': 'testpassword',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        response1 = self.client.post(
            reverse('users:signup'),
            data={
                'username': 'testusername',
                'first_name': 'testname',
                'last_name': 'testname',
                'email': 'test@mail.ru',
                'password': 'testpassword',
            }
        )

        response = self.client.post(
            reverse('users:signup'),
            data={
                'username': 'testusername',
                'first_name': 'testname',
                'last_name': 'testname',
                'email': 'test1@mail.ru',
                'password': 'testpassword',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTest(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru',
        )
        self.db_user.set_password('testpassword')
        self.db_user.save()

    def test_user_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'testpassword',
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')

        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_wrong_error(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser1',
                'password': 'testpassword',

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'testpassword1',

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_profile_redirect(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru',
        )
        user.set_password('testpassword')
        user.save()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_profile_update(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='testname',
            last_name='testname',
            email='test@mail.ru'

        )
        user.set_password('testpassword')
        user.save()

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('users:profile_update'),
            data={
                'username': 'testuser',
                'first_name': 'testname',
                'last_name': 'testlast_name',
                'email': 'test1@mail.ru'
            }
        )

        # user = User.objects.get(pk=user.pk)
        user.refresh_from_db()

        self.assertEqual(user.last_name, 'testlast_name')
        self.assertEqual(user.email, 'test1@mail.ru')
        self.assertEqual(response.url, reverse('users:profile'))
