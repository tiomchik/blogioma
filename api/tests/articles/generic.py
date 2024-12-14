from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class ArticleGenericTestCase(GenericTestCase):
    def _response_contains_article(
        self, r: HttpResponse, article_data: dict, html: bool = False
    ) -> None:
        self.assertContains(r, article_data.get("heading"), html=html)
        self.assertContains(r, article_data.get("full_text"), html=html)
        self.assertContains(r, self.user.username, html=html)

    def _update_article(
        self, pk: int, data: dict, auth: bool = True, token: str = None
    ) -> HttpResponse:
        headers = {}
        if auth:
            headers["Authorization"] = (
                f"Token {token if token else self.token}"
            )

        url = reverse("article-detail", kwargs={"pk": pk})
        r = self.client.put(url, data, headers=headers)

        return r
