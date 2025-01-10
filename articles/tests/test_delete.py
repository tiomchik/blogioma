from .generic import ArticleGenericTestCase
from articles.models import Article


class DeleteArticleTests(ArticleGenericTestCase):
    def test_delete(self) -> None:
        r = self.del_article()
        self.assertEqual(r.status_code, 200)
        self.assertFalse(
            Article.objects.filter(heading=self.article.heading).exists()
        )

    def test_delete_nonuser_article(self) -> None:
        self.auth_to_another_user()

        r = self.del_article()
        self.assertTrue(
            Article.objects.filter(heading=self.article.heading).exists()
        )
