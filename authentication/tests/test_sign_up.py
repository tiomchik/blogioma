from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from authentication.models import User
from main.utils import GenericTestCase


class SignUpTests(GenericTestCase):
    url = reverse("sign_up")
    form_data = {
        "username": "test_user123",
        "password": "12341234",
        "password1": "12341234",
        "email": "test@test.com",
        "captcha_0": "value",
        "captcha_1": "PASSED",
    }

    def test_sign_up(self) -> None:
        self._sign_up_user(self.form_data)
        created_user = User.objects.filter(
            username=self.form_data["username"]
        )
        self.assertTrue(created_user.exists())

    def test_sign_up_without_username(self) -> None:
        self.form_data.pop("username")
        r = self._sign_up_user(self.form_data)
        self.assertContains(r, "This field is required")

    def test_sign_up_without_password(self) -> None:
        self.form_data.pop("password")
        r = self._sign_up_user(self.form_data)
        self.assertContains(r, "This field is required")

    def test_sign_up_with_invalid_email(self) -> None:
        self.form_data["email"] = "invalid_email"
        r = self._sign_up_user(self.form_data)
        self.assertContains(r, "Enter a valid email address")

    def _sign_up_user(self, form_data: dict) -> HttpResponse:
        return self.client.post(
            self.url,
            urlencode(form_data),
            follow=True,
            content_type="application/x-www-form-urlencoded"
        )
