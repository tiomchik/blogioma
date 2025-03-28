from .generic import ArticleGenericTestCase


class CreateArticleTests(ArticleGenericTestCase):
    form_data = {
        "heading": "article test",
        "full_text": "lorem ipsum dolor"
    }

    def test_create(self) -> None:
        self.post_article(self.form_data)
        self.assertArticleExists(heading=self.form_data["heading"])

    def test_unauth_create(self) -> None:
        self.client.logout()
        self.post_article(self.form_data)
        self.assertArticleDoesntExists(heading=self.form_data["heading"])

    def test_create_without_heading(self) -> None:
        self.form_data = {"full_text": "lorem ipsum dolor without heading"}
        self.post_article(self.form_data)
        self.assertArticleDoesntExists(full_text=self.form_data["full_text"])

    def test_create_with_very_long_heading(self) -> None:
        self.form_data["heading"] = "article test" * 10
        self.post_article(self.form_data)
        self.assertArticleDoesntExists(heading=self.form_data["heading"])

    def test_create_without_full_text(self) -> None:
        self.form_data.pop("full_text")
        self.post_article(self.form_data)
        self.assertArticleDoesntExists(heading=self.form_data["heading"])
