from .generic import ArticleGenericTestCase


class UpdateArticleTests(ArticleGenericTestCase):
    article_data = {
        "heading": "test_update_article",
        "full_text": "lorem_ipsum_dolor"
    }

    def test_update(self) -> None:
        r = self.update_article(self.article_data)
        self.assertOkStatus(r)
        self.assertResponseContainsArticle(r, self.article_data)

    def test_update_without_heading(self) -> None:
        self.article_data.pop("heading")
        r = self.update_article(self.article_data)
        self.assertFieldIsRequiredInJson(r, "heading")

    def test_update_with_very_long_heading(self) -> None:
        self.article_data["heading"] = "test_update_article" * 100
        r = self.update_article(self.article_data)
        self.assertFieldIsTooLong(r, "heading")

    def test_update_without_full_text(self) -> None:
        self.article_data.pop("full_text")
        r = self.update_article(self.article_data)
        self.assertFieldIsRequiredInJson(r, "full_text")

    def test_unauth_update(self) -> None:
        self.auth_header = None
        r = self.update_article(self.article_data)
        self.assertUnauthResponse(r)

    def test_update_nonuser_article(self) -> None:
        another_user_data = {
            "username": "test_user2",
            "password": "43214321",
            "email": "test2@test.com"
        }
        self._set_another_user(**another_user_data)
        r = self.update_article(self.article_data)
        self.assertForbiddenResponse(r)
