from urllib.parse import urlencode

from .generic import ArticleGenericTestCase
from articles.models import Article


class CreateArticleTests(ArticleGenericTestCase):
    def test_create(self) -> None:
        heading = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertTrue(Article.objects.filter(heading=heading).exists())

    def test_unauth_create(self) -> None:
        self.client.logout()

        heading = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_create_without_heading(self) -> None:
        full_text = "lorem ipsum dolor without heading"
        data = urlencode({"full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_create_with_very_long_heading(self) -> None:
        heading = "article test" * 10
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_create_without_full_text(self) -> None:
        heading = "article test"
        data = urlencode({"heading": heading})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())
