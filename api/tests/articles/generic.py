from django.http import HttpResponse
from django.urls import reverse

from main.generic_test_cases import APIGenericTestCase


class ArticleGenericTestCase(APIGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()

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

    def post_article(self, data: dict) -> HttpResponse:
        url = reverse("article-list")
        r = self.client.post(url, data, headers=self.auth_header)
        return r

    def update_article(self, data: dict) -> HttpResponse:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.put(url, data, headers=self.auth_header)
        return r

    def delete_article(self) -> HttpResponse:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.delete(url, headers=self.auth_header)
        return r

    def report_article(self, data: dict) -> HttpResponse:
        url = reverse("report-article", kwargs={"pk": self.article.pk})
        r = self.client.post(url, data, headers=self.auth_header)
        return r
