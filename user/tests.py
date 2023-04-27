from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

from .models import User, EmailVerification


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.path = reverse('user:registration')
        self.data = {
            'first_name': 'Danilka',
            'last_name': 'Dyakonov',
            'username': 'mocroper13',
            'email': 'danila-dyakonov@mail.ru',
            'password1': '1q2w3e_VB',
            'password2': '1q2w3e_VB'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'user/registration.html'),
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')

    def test_user_registration_post_success(self):
        username = self.data.get('username')
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('user:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual((now() + timedelta(hours=24)).date(), email_verification.first().expiration.date())

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data.get('username'))
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginTest(TestCase):
    fixtures = ('users.json', )

    def setUp(self):
        self.path = reverse('user:login')
        self.data = {
            'username': 'mocrop13',
            'password': 'Imkd3512#'
        }

    def test_success_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertEqual(response.context_data['title'], 'Store - Авторизация')

    def test_success_login_post(self):
        user = User.objects.get(username=self.data.get('username'))
        assert user.is_authenticated

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

