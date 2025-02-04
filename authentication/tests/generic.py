from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class AuthenticationGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

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

    def set_social_links(
        self, youtube: str = "https://www.youtube.com/",
        tiktok: str = "https://tiktok.com/",
        twitch: str = "https://twitch.tv/",
        linkedin: str = "https://linkedin.com/"
    ) -> HttpResponse:
        url = reverse(
            "social_media_links", kwargs={"username": self.user.username}
        )
        data = urlencode({
            "youtube": youtube, "tiktok": tiktok, "twitch": twitch,
            "linkedin": linkedin
        })
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )
        self.user.refresh_from_db()

        return r

    def assertUserIsAuthenticated(self, r: HttpResponse) -> None:
        self.assertTrue(r.context["user"].is_authenticated)

    def assertUserIsNotAuthenticated(self, r: HttpResponse) -> None:
        self.assertFalse(r.context["user"].is_authenticated)

    def assertFieldIsRequiredOnPage(self, r: HttpResponse) -> None:
        self.assertContains(r, "This field is required")
