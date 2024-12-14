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
        r = self._register_user(**self.user_data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json().get("username"), ["This field is required."])

    def test_register_without_password(self) -> None:
        self.user_data.pop("password")
        r = self._register_user(**self.user_data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json().get("password"), ["This field is required."])

    def test_register_with_pfp(self) -> None:
        with open("api/tests/authentication/cat.jpg", "rb") as picture:
            pfp = SimpleUploadedFile(
                "cat.jpg", picture.read(), content_type="image/jpeg"
            )

        self.user_data["pfp"] = pfp
        r = self.client.post(self.url, self.user_data, format="multipart")
        self.user.refresh_from_db()

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.user.pfp)
