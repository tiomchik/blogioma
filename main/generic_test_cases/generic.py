from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APITestCase

from articles.models import Article
from comments.models import Comment


class GenericTestCase(APITestCase):
    def register_user(self, **user_data) -> HttpResponse:
        url = reverse("register")
        return self.client.post(url, user_data)

    def load_pfp(self, path: str) -> SimpleUploadedFile:
        with open(path, "rb") as picture:
            return SimpleUploadedFile(
                "cat.jpg", picture.read(), content_type="image/jpeg"
            )

    def assertResponseContainsArticles(
        self, r: HttpResponse, articles: list[Article]
    ) -> None:
        for article in articles:
            self.assertContains(r, article.heading)

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
