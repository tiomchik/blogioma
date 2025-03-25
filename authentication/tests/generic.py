from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from main.generic_test_cases import SessionAuthGenericTestCase


class AuthenticationGenericTestCase(SessionAuthGenericTestCase):
    def sign_up_user(self, form_data: dict) -> HttpResponse:
        url = reverse("sign_up")
        return self.client.post(
            url,
            urlencode(form_data),
            follow=True,
            content_type="application/x-www-form-urlencoded"
        )

    def login_user(self, form_data: dict) -> HttpResponse:
        url = reverse("log_in")
        return self.client.post(
            url,
            urlencode(form_data),
            follow=True,
            content_type="application/x-www-form-urlencoded"
        )

    def set_and_refresh_social_links(self, data: dict) -> HttpResponse:
        url = reverse(
            "social_media_links", kwargs={"username": self.user.username}
        )
        data = urlencode(data)
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )
        self.user.refresh_from_db()

        return r

    def get_profile_page(self) -> HttpResponse:
        url = reverse("profile", kwargs={"username": self.user.username})
        return self.client.get(url)

    def change_pfp(self, pfp: SimpleUploadedFile) -> HttpResponse:
        url = reverse("change_pfp")
        return self.client.post(
            url, {"new_pfp": pfp}, follow=True, format="multipart"
        )

    def change_username(self, username: str) -> HttpResponse:
        data = urlencode({
            "new_username": username,
            "captcha_0": "value",
            "captcha_1": "PASSED"
        })
        url = reverse("change_username")
        return self.client.post(
            url, data, follow=True,
            content_type="application/x-www-form-urlencoded"
        )

    def change_password(
        self, password: str, confirm_password: str
    ) -> HttpResponse:
        data = urlencode({
            "new_password": password, "new_password1": confirm_password,
            "captcha_0": "value", "captcha_1": "PASSED"
        })
        url = reverse("change_password")
        return self.client.post(
            url, data, content_type="application/x-www-form-urlencoded"
        )

    def assertUserIsAuthenticated(self, r: HttpResponse) -> None:
        self.assertTrue(r.context["user"].is_authenticated)

    def assertUserIsNotAuthenticated(self, r: HttpResponse) -> None:
        self.assertFalse(r.context["user"].is_authenticated)

    def assertFieldIsRequiredOnPage(self, r: HttpResponse) -> None:
        self.assertContains(r, "This field is required")
