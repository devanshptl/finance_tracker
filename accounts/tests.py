from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class RegisterUserTest(APITestCase):

    def test_register(self):
        data = {
            "username": "testuser",
            "email": "abc@gmail.com",
            "password": "abc@123",
            "password2": "abc@123",
        }

        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutUserTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="ex", password="qw@123")

    def test_login(self):
        data = {"username": "ex", "password": "qw@123"}

        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="ex")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
