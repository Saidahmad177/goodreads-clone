from django.contrib.auth import get_user
from django.contrib.auth.models import User
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

        user = User.objects.get(username='testuser')

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
        user_count = User.objects.count()

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
        user_count = User.objects.count()
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

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTest(TestCase):
    def test_user_login(self):
        db_user = User.objects.create(username='testuser')
        db_user.set_password('testpassword')
        db_user.save()

        self.client.post(
            reverse('users:login_page'),
            data={
                'username': 'testuser',
                'password': 'testpassword',
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_error(self):
        db_user = User.objects.create(username='testuser')
        db_user.set_password('testpassword')
        db_user.save()

        self.client.post(
            reverse('users:login_page'),
            data={
                'username': 'testuser1',
                'password': 'testpassword',

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login_page'),
            data={
                'username': 'testuser',
                'password': 'testpassword1',

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
