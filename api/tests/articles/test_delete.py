from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class DeleteArticleTests(ArticleGenericTestCase):
    def test_delete(self) -> None:
        url = self._get_article_detail_url()
        r = self.client.delete(url, headers=self.auth_header)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            r.json().get("detail"), "No Article matches the given query."
        )

    def test_delete_nonuser_article(self) -> None:
        another_user_data = {
            "username": "test_user3",
            "password": "43214321",
            "email": "test3@test.com"
        }
        self._set_another_user(**another_user_data)

        url = self._get_article_detail_url()
        r = self.client.delete(url, headers=self.auth_header)
        self._assert_forbidden_response(r)

    def _get_article_detail_url(self) -> str:
        return reverse("article-detail", kwargs={"pk": self.article.pk})
