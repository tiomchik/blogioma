from .generic import ArticleGenericTestCase


class DeleteArticleTests(ArticleGenericTestCase):
    def test_delete(self) -> None:
        r = self.del_article()
        self.assertEqual(r.status_code, 200)
        self.assertArticleDoesntExists(heading=self.article.heading)

    def test_delete_nonuser_article(self) -> None:
        self.auth_to_another_user()
        self.del_article()
        self.assertArticleExists(heading=self.article.heading)
