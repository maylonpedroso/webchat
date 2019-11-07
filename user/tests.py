from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserLoginTestCase(TestCase):

    def setUp(self) -> None:
        self.login_url = reverse('user:login')

    def _createTestUser(self):
        user = User(username='test_user')
        user.set_password('test_password')
        user.save()
        self.addCleanup(user.delete)

    def test_login_form_displays_for_anonymous_user(self):
        response = self.client.get(self.login_url)

        self.assertContains(response, '<title>Login</title>')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')

    def test_login_redirects_to_home_for_logged_in_user(self):
        self._createTestUser()

        response = self.client.post(
            self.login_url, {'username': 'test_user', 'password': 'test_password'}
        )

        self.assertRedirects(response, '/', 302)

    def test_login_displays_again_for_invalid_credentials(self):
        self._createTestUser()

        response = self.client.post(
            self.login_url, {'username': 'test_user', 'password': 'wrong_password'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Login</title>')


class UserSignupTestCase(TestCase):

    def setUp(self) -> None:
        self.signup_url = reverse('user:signup')
        self.login_url = reverse('user:login')

    def test_signup_page_renders(self):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Sign Up</title>')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Password confirmation')

    def test_user_created_for_valid_credentials(self):
        credentials = {
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'test_password',
        }

        response = self.client.post(self.signup_url, credentials)

        user = User.objects.get(username=credentials['username'])

        self.assertIsNotNone(user)
        self.assertRedirects(response, self.login_url, 302)

        user.delete()

    def test_user_is_not_created_on_invalid_credentials(self):
        credentials = {
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'wrong_password',
        }

        response = self.client.post(self.signup_url, credentials)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=credentials['username'])

        self.assertEqual(response.status_code, 200)
