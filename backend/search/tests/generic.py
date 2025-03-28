from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.generic_test_cases import SessionAuthGenericTestCase


class SearchGenericTestCase(SessionAuthGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()

    def search(self, query: str) -> HttpResponse:
        url = reverse("search")
        r = self.client.post(
            url, urlencode({"search_query": query}),
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r
