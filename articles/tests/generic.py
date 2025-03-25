from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from articles.models import Article
from main.generic_test_cases import SessionAuthGenericTestCase


class ArticleGenericTestCase(SessionAuthGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()

    def post_article(self, data: dict) -> HttpResponse:
        url = reverse("add_article")
        r = self.client.post(
            url, urlencode(data),
            content_type="application/x-www-form-urlencoded", follow=True
        )
        return r

    def update_article(self, data: dict) -> HttpResponse:
        url = reverse("update", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, urlencode(data),
            content_type="application/x-www-form-urlencoded", follow=True
        )
        return r

    def del_article(self) -> HttpResponse:
        url = reverse("delete", kwargs={"pk": self.article.pk})
        r = self.client.get(url, follow=True)
        return r

    def assertArticleExists(self, **filter_kwargs) -> None:
        self.assertTrue(Article.objects.filter(**filter_kwargs).exists())

    def assertArticleDoesntExists(self, **filter_kwargs) -> None:
        self.assertFalse(Article.objects.filter(**filter_kwargs).exists())

    def assertPageContainsArticle(
        self, r: HttpResponse, article: Article
    ) -> None:
        self.assertContains(r, article.heading)
        self.assertContains(r, article.full_text)
        self.assertContains(r, article.author.username)
