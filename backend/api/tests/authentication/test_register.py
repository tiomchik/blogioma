from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class RegisterTests(AuthenticationGenericTestCase):
    url = reverse("register")

    def setUp(self) -> None:
        super().setUp()
        self.user_data = {
            "username": "test_user123",
            "password": "12341234",
        }

    def test_register_without_username(self) -> None:
        self.user_data.pop("username")
        r = self.register_user(**self.user_data)
        self.assertFieldIsRequiredInJson(r, "username")

    def test_register_without_password(self) -> None:
        self.user_data.pop("password")
        r = self.register_user(**self.user_data)
        self.assertFieldIsRequiredInJson(r, "password")

    def test_register_with_pfp(self) -> None:
        self.user_data["pfp"] = self.load_pfp("api/tests/authentication/cat.jpg")
        r = self.client.post(self.url, self.user_data, format="multipart")
        self.user.refresh_from_db()

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.user.pfp)

    def test_register_with_busy_email(self) -> None:
        another_user_data = {
            "username": "another_user",
            "password": "12341234",
            "email": "test@example.com"
        }
        self.register_user(**another_user_data)
        self.user_data["email"] = another_user_data["email"]

        r = self.register_user(**self.user_data)

        self.assertEqual(r.json()["email"], ["This email is already busy"])
