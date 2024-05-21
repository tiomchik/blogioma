from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import Profile
from articles.models import Article
from comments.models import Comment


class GenericTestCase(APITestCase):
    def setUp(self) -> None:
        data = {"username": "test_user1", "password": "12341234"}
        self._register_user(**data)

        self.user = User.objects.get(username=data["username"])
        self.profile = Profile.objects.get(user=self.user)
        self.token = self._obtain_token(**data)

        self.article = self._create_article()
        self.comment = Comment.objects.create(
            text="nice article", article=self.article, profile=self.profile
        )

    def _obtain_token(self, **user_data) -> str:
        """Obtains token according to passed `user_data`."""
        token_url = reverse("obtain-token")
        token: str = self.client.post(
            token_url, user_data
        ).json().get("token")

        return token

    def _register_user(self, **user_data) -> HttpResponse:
        """Registers a user with `user_data`."""
        url = reverse("register")
        return self.client.post(url, user_data)

    def _check_unauth_response(self, r: HttpResponse) -> None:
        """Checks that response is returned error of unauthorized user."""
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            r.json().get("detail"),
            "Authentication credentials were not provided."
        )

    def _create_article(
        self, headling: str = "test_article",
        full_text: str = "lorem ipsum dolor"
    ) -> Article:
        """Creates article and returns it."""
        data = {
            "headling": headling, "full_text": full_text,
            "author": self.profile
        }
        return Article.objects.create(**data)