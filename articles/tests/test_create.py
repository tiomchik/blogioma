from urllib.parse import urlencode

from .generic import ArticleGenericTestCase
from articles.models import Article


class CreateArticleTests(ArticleGenericTestCase):
    form_data = {
        "heading": "article test",
        "full_text": "lorem ipsum dolor"
    }

    def test_create(self) -> None:
        self.post_article(urlencode(self.form_data))
        self.assertTrue(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_unauth_create(self) -> None:
        self.client.logout()
        self.post_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_create_without_heading(self) -> None:
        self.form_data = {"full_text": "lorem ipsum dolor without heading"}
        self.post_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(
                full_text=self.form_data["full_text"]
            ).exists()
        )

    def test_create_with_very_long_heading(self) -> None:
        self.form_data["heading"] = "article test" * 10
        self.post_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_create_without_full_text(self) -> None:
        self.form_data.pop("full_text")
        self.post_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )
