from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class SearchGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def search(self, query: str) -> HttpResponse:
        url = reverse("search")
        r = self.client.post(
            url, urlencode({"search_query": query}),
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r
