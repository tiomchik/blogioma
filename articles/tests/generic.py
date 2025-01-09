from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class ArticleGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def _post_article(self, encoded_data: str) -> HttpResponse:
        """Creates an article using POST."""
        url = reverse("add_article")
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def _update_article(self, encoded_data: str) -> HttpResponse:
        """Updates an article using POST."""
        url = reverse("update", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def _del_article(self) -> HttpResponse:
        """Deletes an article using GET."""
        url = reverse("delete", kwargs={"pk": self.article.pk})
        r = self.client.get(url, follow=True)

        return r
