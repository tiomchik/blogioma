from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponse

from main.utils import GenericTestCase


class AuthenticationGenericTestCase(GenericTestCase):
    def set_and_refresh_social_links(self, data: dict) -> HttpResponse:
        url = reverse("edit-me")
        r = self.client.put(url, data, headers=self.auth_header)

        self.user.refresh_from_db()
        cache.clear()

        return r

    def update_user_data(self, data: dict) -> HttpResponse:
        url = reverse("edit-me")
        r = self.client.put(url, data, headers=self.auth_header)
        return r
