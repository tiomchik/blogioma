from django.urls import reverse
from django.http import HttpResponse

from main.generic_test_cases import APIGenericTestCase


class AuthenticationGenericTestCase(APIGenericTestCase):
    def set_and_refresh_social_links(self, data: dict) -> HttpResponse:
        url = reverse("edit-me")
        r = self.client.put(url, data, headers=self.auth_header)

        self.user.refresh_from_db()

        return r

    def update_user_data(self, data: dict) -> HttpResponse:
        url = reverse("edit-me")
        r = self.client.put(url, data, headers=self.auth_header)
        return r

    def get_me(self) -> HttpResponse:
        url = reverse("me")
        r = self.client.get(url, headers=self.auth_header)
        return r
