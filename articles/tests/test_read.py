from django.urls import reverse

from .generic import ArticleGenericTestCase


class ReadArticleTests(ArticleGenericTestCase):
    def test_read_at_home_page(self) -> None:
        url = reverse("home")
        r = self.client.get(url)

        self.assertContains(r, self.article.heading)

    def test_read_detail(self) -> None:
        url = reverse("read", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.article.heading)
        self.assertContains(r, self.article.full_text)
        self.assertContains(r, self.article.author.username)

    def test_random(self) -> None:
        url = reverse("random_article")
        r = self.client.get(url, follow=True)

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, self.article.full_text)
