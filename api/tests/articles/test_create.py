from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class CreateArticleTests(ArticleGenericTestCase):
    url = reverse("article-list")
    article_data = {
        "heading": "lorem ipsum dolor",
        "full_text": "lorem ipsum dolor test"
    }

    def test_create(self) -> None:
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self._assert_response_contains_article(r, self.article_data)

    def test_unauth_create(self) -> None:
        r = self.client.post(self.url, self.article_data)
        self._assert_unauth_response(r)

    def test_create_without_heading(self) -> None:
        self.article_data.pop("heading")
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )
        self._assert_field_is_required(r, "heading")

    def test_create_with_very_long_heading(self) -> None:
        self.article_data["heading"] = "lorem ipsum dolor" * 100
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )
        self._assert_field_is_too_long(r, "heading")

    def test_create_without_full_text(self) -> None:
        self.article_data.pop("full_text")
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )
        self._assert_field_is_required(r, "full_text")
