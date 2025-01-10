from urllib.parse import urlencode

from .generic import ArticleGenericTestCase
from articles.models import Article


class UpdateArticleTests(ArticleGenericTestCase):
    def setUp(self):
        super().setUp()
        self.form_data = {
            "heading": "updated article",
            "full_text": "new lorem ipsum dolor"
        }

    def test_update(self) -> None:
        self.update_article(urlencode(self.form_data))
        self.assertArticleExists(heading=self.form_data["heading"])

    def test_update_without_heading(self) -> None:
        self.form_data.pop("heading")
        self.update_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(
                full_text=self.form_data["full_text"]
            ).exists()
        )

    def test_update_with_very_long_heading(self) -> None:
        self.form_data["heading"] = "updated article" * 10
        self.update_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_update_without_full_text(self) -> None:
        self.form_data.pop("full_text")
        self.update_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_unauth_update(self) -> None:
        self.client.logout()
        self.update_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )

    def test_update_nonuser_article(self) -> None:
        self.auth_to_another_user()
        self.update_article(urlencode(self.form_data))
        self.assertFalse(
            Article.objects.filter(heading=self.form_data["heading"]).exists()
        )
