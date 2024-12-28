from rest_framework import status
from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class ArticleGenericTestCase(GenericTestCase):
    def assertResponseContainsArticle(
        self, r: HttpResponse, article_data: dict
    ) -> None:
        self.assertContains(
            r, article_data.get("heading"), status_code=r.status_code
        )
        self.assertContains(
            r, article_data.get("full_text"), status_code=r.status_code
        )
        self.assertContains(r, self.user.username, status_code=r.status_code)

    def _update_article(self, data: dict) -> HttpResponse:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.put(url, data, headers=self.auth_header)
        return r
