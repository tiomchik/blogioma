from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class ArticleGenericTestCase(GenericTestCase):
    def _response_contains_article(
        self, r: HttpResponse, article_data: dict
    ) -> None:
        self.assertContains(r, article_data.get("heading"))
        self.assertContains(r, article_data.get("full_text"))
        self.assertContains(r, self.user.username)

    def _update_article(self, data: dict) -> HttpResponse:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.put(url, data, headers=self.authorization_header)
        return r
