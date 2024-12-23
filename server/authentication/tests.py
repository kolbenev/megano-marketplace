import json

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status

from userprofile.models import UserProfile


class TestSignIn(TestCase):

    def setUp(self):
        self.url = reverse('sign-in')
        self.username = "testuser"
        self.password = "testpassword123"
        User.objects.create_user(username=self.username, password=self.password)

    def test_successful_sign_in(self):
        """
        Тестирование успешной авторизации.
        """
        data = {
            json.dumps({
                "username": self.username,
                "password": self.password,
            }): ""
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_username(self):
        """
        Тестирование авторизации без указания имени пользователя.
        """
        data = {
            json.dumps({
                "username": "",
                "password": self.password,
            }): ""
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password(self):
        """
        Тестирование авторизации без указания пароля.
        """
        data = {
            json.dumps({
                "username": self.username,
                "password": "",
            }): ""
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_credentials(self):
        """
        Тестирование авторизации с неверными учетными данными.
        """
        data = {
            json.dumps({
                "username": self.username,
                "password": "wrong-password",
            }): ""
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_data(self):
        """
        Тестирование авторизации с некорректными данными.
        """
        payload = "invalid_payload"
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestSignOut(TestCase):
    def setUp(self):
        self.url = reverse('sign-out')
        self.username = "testuser"
        self.password = "password"

        self.new_user = User.objects.create(
            username=self.username,
            password=self.password,
        )

        self.client.login(username=self.username, password=self.password)

    def test_successful_sign_out(self):
        """Тест успешного выхода из системы."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_out_invalid_method(self):
        """Тест выхода с использованием некорректного HTTP-метода."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse('sign-up')

    def test_successful_sign_up(self):
        """
        Тестирование успешной регистрации нового пользователя.
        """
        payload = {
            json.dumps({"username": "newuser", "password": "newpassword123", "name": "New User"}): ""
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_sign_up_missing_name(self):
        """
        Тестирование регистрации пользователя без имени.
        """
        payload = {
            json.dumps({"username": "newuser", "password": "newpassword123", "name": None}): ""
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user_profile = UserProfile.objects.get(user__username="newuser")
        self.assertEqual(user_profile.fullName, "nameless")

    def test_sign_up_missing_username(self):
        """
        Тестирование регистрации пользователя без имени пользователя.
        """
        payload = {
            json.dumps({"password": "newpassword123", "name": "New User"}): ""
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_missing_password(self):
        """
        Тестирование регистрации пользователя без пароля.
        """
        payload = {
            json.dumps({"username": "newuser", "name": "New User"}): ""
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_invalid_data(self):
        """
        Тестирование регистрации с некорректными данными.
        """
        payload = "invalid_payload"
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
