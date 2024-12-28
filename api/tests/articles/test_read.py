from django.urls import reverse

from .generic import ArticleGenericTestCase


class ReadArticleTests(ArticleGenericTestCase):
    article_data = {
        "heading": "test_article_read",
        "full_text": "lorem ipsum dolor",
    }

    def setUp(self):
        super().setUp()
        self.article = self.create_article(**self.article_data)

    def test_read_list(self) -> None:
        url = reverse("article-list")
        r = self.client.get(url)
        self.assertResponseContainsArticle(r, self.article_data)

    def test_read_detail(self) -> None:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.get(url)
        self.assertResponseContainsArticle(r, self.article_data)

    def test_search(self) -> None:
        url = reverse("article-list") + f"?q={self.article_data["heading"]}"
        r = self.client.get(url)
        self.assertResponseContainsArticle(r, self.article_data)

    def test_random(self) -> None:
        for i in range(10):
            self.create_article(heading=f"test_article{i}")

        url = reverse("article-random-article")
        r = self.client.get(url)

        self.assertOkStatus(r)
        self.assertIsNotNone(r.json().get("heading"))
        self.assertIsNotNone(r.json().get("full_text"))
        self.assertIsNotNone(r.json().get("author"))
