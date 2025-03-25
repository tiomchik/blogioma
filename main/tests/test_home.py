from .generic import MainGenericTestCase


class HomeTests(MainGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()

    def test_home(self) -> None:
        r = self.get_home_page()
        self.assertContains(r, self.article.heading)

    def test_home_with_list_of_articles(self) -> None:
        articles = self.create_list_of_articles(5)
        r = self.get_home_page()
        self.assertResponseContainsArticles(r, articles)
