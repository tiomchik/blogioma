from urllib.parse import urlencode

from .generic import ArticleGenericTestCase
from articles.models import Article


class UpdateArticleTests(ArticleGenericTestCase):
    def test_update(self) -> None:
        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertTrue(Article.objects.filter(heading=heading).exists())

    def test_update_without_heading(self) -> None:
        full_text = "new lorem ipsum dolor"
        data = urlencode({"full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_update_with_very_long_heading(self) -> None:
        heading = "updated article" * 10
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_update_without_full_text(self) -> None:
        heading = "updated article"
        data = urlencode({"heading": heading})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_unauth_update(self) -> None:
        self.client.logout()

        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_update_nonuser_article(self) -> None:
        self.auth_to_another_user()

        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())
