from django.urls import reverse
from rest_framework import status

from .generic import ArticleGenericTestCase


class DeleteArticleTests(ArticleGenericTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("article-detail", kwargs={"pk": self.article.pk})

    def test_delete(self) -> None:
        r = self.delete_article()
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.client.get(self.url)
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
        r = self.delete_article()
        self.assertForbiddenResponse(r)
