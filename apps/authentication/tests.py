from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.authentication.models import User


class AuthenticationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@ex.com", password="Qwerty@123")

    def test_signup(self):
        url = reverse("authentication-signup")
        data = {"email": "test_1@ex.com", "password": "Qwerty@123"}

        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["email"], "test_1@ex.com")

    def test_login(self):
        url = reverse("authentication-login")

        r = self.client.post(url, {"email": self.user.email, "password": "Qwerty@123"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue(r.data.get("token"))

    def test_logout(self):
        login_url = reverse("authentication-login")
        logout_url = reverse("authentication-logout")

        r = self.client.post(logout_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        token = self.client.post(
            login_url, {"email": self.user.email, "password": "Qwerty@123"}
        ).data["token"]
        r = self.client.post(logout_url, HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)


class ProfileViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@ex.com", password="Qwerty@123")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_retrieve(self):
        url = reverse("profile")

        r = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, {"email": "test@ex.com", "first_name": "", "last_name": ""})

    def test_update(self):
        url = reverse("profile")

        r = self.client.patch(
            url,
            {"first_name": "Sam", "last_name": "Winston"},
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(
            r.data, {"email": "test@ex.com", "first_name": "Sam", "last_name": "Winston"}
        )
