from django.urls import reverse

from main.generic_test_cases import SessionAuthGenericTestCase


class HomeTests(SessionAuthGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()

    url = reverse("home")

    def test_home(self) -> None:
        r = self.client.get(self.url)
        self.assertContains(r, self.article.heading)

    def test_home_with_list_of_articles(self) -> None:
        articles = self.create_list_of_articles(5)
        r = self.client.get(self.url)
        self.assertResponseContainsArticles(r, articles)
