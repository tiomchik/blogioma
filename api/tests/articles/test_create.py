from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class CreateArticleTests(ArticleGenericTestCase):
    url = reverse("article-list")

    def test_create(self) -> None:
        data = {
            "heading": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            self.url, data, headers=self.authorization_header
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("heading"), data["heading"])
        self.assertEqual(r.json().get("full_text"), data["full_text"])
        self.assertEqual(
            r.json().get("author").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        data = {
            "heading": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(self.url, data)

        self._check_unauth_response(r)

    def test_create_without_heading(self) -> None:
        data = {"full_text": "lorem ipsum dolor test"}
        r = self.client.post(
            self.url, data, headers=self.authorization_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"), ["This field is required."]
        )

    def test_create_with_very_long_heading(self) -> None:
        data = {
            "heading": "lorem ipsum dolorrrrrrrrrrrrrrrrrrrrrrr" * 10,
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            self.url, data, headers=self.authorization_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"),
            ["Ensure this field has no more than 100 characters."]
        )

    def test_create_without_full_text(self) -> None:
        data = {"heading": "lorem ipsum dolor"}
        r = self.client.post(
            self.url, data, headers=self.authorization_header
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )
