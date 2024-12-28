from django.urls import reverse
from django.http import HttpResponse
from django.core.cache import cache

from articles.models import Article
from main.utils import GenericTestCase


class HomeTests(GenericTestCase):
    url = reverse("home")

    def test_home(self) -> None:
        r = self.client.get(self.url)
        self.assertContains(r, self.article.heading)

    def test_home_with_list_of_articles(self) -> None:
        articles = self.create_list_of_articles()
        cache.clear()
        r = self.client.get(self.url)
        self.assertResponseContainsArticles(r, articles)

    def create_list_of_articles(self) -> list[Article]:
        articles = []
        for i in range(5):
            article = self.create_article(f"test_article_{i}")
            articles.append(article)

        return articles

    def assertResponseContainsArticles(
        self, r: HttpResponse, articles: list[Article]
    ) -> None:
        for article in articles:
            self.assertContains(r, article.heading)
