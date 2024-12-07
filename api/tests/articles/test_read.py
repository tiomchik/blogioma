from django.urls import reverse
from rest_framework import status

from articles.models import Article
from .generic import ArticleGenericTestCase


class ReadArticleTests(ArticleGenericTestCase):
    def test_read_list(self) -> None:
        data = {
            "heading": "test_article_list",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        Article.objects.create(**data)

        url = reverse("article-list")
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_read_detail(self) -> None:
        data = {
            "heading": "test_article_detail",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        article = Article.objects.create(**data)

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_search(self) -> None:
        data = {
            "heading": "find_me",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        Article.objects.create(**data)

        url = reverse("article-list") + f"?q={data.get('heading')}"
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_random(self) -> None:
        for i in range(10):
            self._create_article(heading=f"test_article{i}")

        url = reverse("article-random-article")
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(r.json().get("heading"))
        self.assertIsNotNone(r.json().get("full_text"))
        self.assertIsNotNone(r.json().get("author"))
