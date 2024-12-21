from django.urls import reverse
from rest_framework import status

from articles.models import Article
from .generic import ArticleGenericTestCase


class ReadArticleTests(ArticleGenericTestCase):
    article_data = {
        "heading": "test_article_read",
        "full_text": "lorem ipsum dolor",
    }

    def test_read_list(self) -> None:
        Article.objects.create(**self.article_data, author=self.user)

        url = reverse("article-list")
        r = self.client.get(url)

        self._assert_response_contains_article(r, self.article_data)

    def test_read_detail(self) -> None:
        article = Article.objects.create(**self.article_data, author=self.user)

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.get(url)

        self._assert_response_contains_article(r, self.article_data)

    def test_search(self) -> None:
        Article.objects.create(**self.article_data, author=self.user)

        url = reverse("article-list") + f"?q={self.article_data["heading"]}"
        r = self.client.get(url)

        self._assert_response_contains_article(r, self.article_data)

    def test_random(self) -> None:
        for i in range(10):
            self._create_article(heading=f"test_article{i}")

        url = reverse("article-random-article")
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(r.json().get("heading"))
        self.assertIsNotNone(r.json().get("full_text"))
        self.assertIsNotNone(r.json().get("author"))
