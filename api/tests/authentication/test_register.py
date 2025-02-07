from django.core.files.uploadedfile import SimpleUploadedFile
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
