from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class DeleteArticleTests(ArticleGenericTestCase):
    def test_delete(self) -> None:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {self.token}"}
        )
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
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)

        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {another_user_token}"}
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
