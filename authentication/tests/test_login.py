from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class LoginTests(GenericTestCase):
    url = reverse("log_in")
    form_data = {
        "username": "test_user123",
        "password": "12341234",
        "captcha_0": "value",
        "captcha_1": "PASSED",
    }

    def setUp(self) -> None:
        super().setUp()
        self.register_user(**self.form_data)

    def test_login(self) -> None:
        r = self.login_user(self.form_data)
        self.assertUserIsAuthenticated(r)

    def test_login_without_username(self) -> None:
        self.form_data.pop("username")
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_without_password(self) -> None:
        self.form_data.pop("password")
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_with_invalid_username(self) -> None:
        self.form_data["username"] = "invalid_username"
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_with_invalid_password(self) -> None:
        self.form_data["password"] = "invalid_password"
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def login_user(self, form_data: dict) -> HttpResponse:
        return self.client.post(
            self.url,
            urlencode(form_data),
            follow=True,
            content_type="application/x-www-form-urlencoded"
        )

    def assertUserIsAuthenticated(self, r: HttpResponse) -> None:
        self.assertTrue(r.context["user"].is_authenticated)

    def assertUserIsNotAuthenticated(self, r: HttpResponse) -> None:
        self.assertFalse(r.context["user"].is_authenticated)
