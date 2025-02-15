from django.urls import reverse

from .generic import ArticleGenericTestCase


class ReadArticleTests(ArticleGenericTestCase):
    def test_read_at_home_page(self) -> None:
        url = reverse("home")
        r = self.client.get(url)
        self.assertPageContainsArticle(r, self.article)

    def test_read_detail(self) -> None:
        url = reverse("read", kwargs={"pk": self.article.pk})
        r = self.client.get(url)
        self.assertPageContainsArticle(r, self.article)

    def test_random(self) -> None:
        url = reverse("random_article")
        r = self.client.get(url, follow=True)
        self.assertPageContainsArticle(r, self.article)

    def test_see_all_latest(self) -> None:
        url = reverse("see_all", kwargs={"order_by": "latest"})
        r = self.client.get(url)
        self.assertPageContainsArticle(r, self.article)

    def test_see_all_popular(self) -> None:
        url = reverse("see_all", kwargs={"order_by": "popular"})
        r = self.client.get(url)
        self.assertPageContainsArticle(r, self.article)
