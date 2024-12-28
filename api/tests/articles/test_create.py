from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class CreateArticleTests(ArticleGenericTestCase):
    article_data = {
        "heading": "lorem ipsum dolor",
        "full_text": "lorem ipsum dolor test"
    }

    def test_create(self) -> None:
        r = self.post_article(self.article_data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertResponseContainsArticle(r, self.article_data)

    def test_unauth_create(self) -> None:
        self.auth_header = {}
        r = self.post_article(self.article_data)
        self.assertUnauthResponse(r)

    def test_create_without_heading(self) -> None:
        self.article_data.pop("heading")
        r = self.post_article(self.article_data)
        self.assertFieldIsRequired(r, "heading")

    def test_create_with_very_long_heading(self) -> None:
        self.article_data["heading"] = "lorem ipsum dolor" * 100
        r = self.post_article(self.article_data)
        self.assertFieldIsTooLong(r, "heading")

    def test_create_without_full_text(self) -> None:
        self.article_data.pop("full_text")
        r = self.post_article(self.article_data)
        self.assertFieldIsRequired(r, "full_text")
