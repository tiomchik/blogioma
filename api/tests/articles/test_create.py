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
        self.assertEqual(
            r.json().get("heading"), self.article_data["heading"]
        )
        self.assertEqual(
            r.json().get("full_text"), self.article_data["full_text"]
        )
        self.assertEqual(
            r.json().get("author").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        r = self.client.post(self.url, self.article_data)
        self._check_unauth_response(r)

    def test_create_without_heading(self) -> None:
        self.article_data.pop("heading")
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"), ["This field is required."]
        )

    def test_create_with_very_long_heading(self) -> None:
        self.article_data["heading"] = "lorem ipsum dolor" * 100
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"),
            ["Ensure this field has no more than 100 characters."]
        )

    def test_create_without_full_text(self) -> None:
        self.article_data.pop("full_text")
        r = self.client.post(
            self.url, self.article_data, headers=self.auth_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )
