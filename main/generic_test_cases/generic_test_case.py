from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from articles.models import Article
from comments.models import Comment


class GenericTestCase(APITestCase):
    def setUp(self) -> None:
        data = {"username": "test_user1", "password": "12341234"}
        self.register_user(**data)

        self.user = User.objects.get(username=data["username"])
        self.token = self._obtain_token(**data)
        self.auth_header = {"Authorization": f"Token {self.token}"}

    def setUpSessionAuth(self) -> None:
        user_data = {"username": "test_user", "password": "12341234"}
        self.user = User.objects.create_user(**user_data)
        self.client.login(**user_data)

    def _obtain_token(self, **user_data) -> str:
        token_url = reverse("obtain-token")
        token: str = self.client.post(
            token_url, user_data
        ).json().get("token")

        return token

    def register_user(self, **user_data) -> HttpResponse:
        url = reverse("register")
        return self.client.post(url, user_data)

    def _set_another_user(self, **another_user_data) -> None:
        self.register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)
        self.auth_header = {
            "Authorization": f"Token {another_user_token}"
        }

    def load_pfp(self, path: str) -> SimpleUploadedFile:
        with open(path, "rb") as picture:
            return SimpleUploadedFile(
                "cat.jpg", picture.read(), content_type="image/jpeg"
            )

    def assertUnauthResponse(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            r.json().get("detail"),
            "Authentication credentials were not provided."
        )

    def assertFieldIsRequiredInJson(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get(field), ["This field is required."]
        )

    def assertFieldIsTooLong(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        error: str = r.json().get(field)[0]
        self.assertTrue(error.startswith("Ensure this field has no more"))
        self.assertTrue(error.endswith(" characters."))

    def assertForbiddenResponse(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    def assertResponseContainsArticles(
        self, r: HttpResponse, articles: list[Article]
    ) -> None:
        for article in articles:
            self.assertContains(r, article.heading)

    def assertContainsList(self, r: HttpResponse, list: list) -> None:
        for item in list:
            self.assertContains(r, item)

    def assertNotContainsList(self, r: HttpResponse, list: list) -> None:
        for item in list:
            self.assertNotContains(r, item)

    def assertOkStatus(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def auth_to_another_user(
        self, username: str = "test_user123", password: str = "12341234"
    ) -> None:
        self.client.logout()
        new_user_data = {"username": username, "password": password}
        User.objects.create(**new_user_data)
        self.client.login(**new_user_data)

    def create_article(
        self, heading: str = "test_article",
        full_text: str = "lorem ipsum dolor"
    ) -> Article:
        data = {
            "heading": heading, "full_text": full_text,
            "author": self.user
        }
        return Article.objects.create(**data)

    def create_list_of_articles(self, quantity: int) -> list[Article]:
        articles = []
        for i in range(quantity):
            article = self.create_article(f"test_article_{i}")
            articles.append(article)

        return articles

    def create_comment(
        self, article: Article, text: str = "nice article"
    ) -> Comment:
        data = {"article": article, "author": self.user, "text": text}
        return Comment.objects.create(**data)
