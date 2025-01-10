from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class ArticleGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def post_article(self, encoded_data: str) -> HttpResponse:
        url = reverse("add_article")
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def update_article(self, encoded_data: str) -> HttpResponse:
        url = reverse("update", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def del_article(self) -> HttpResponse:
        url = reverse("delete", kwargs={"pk": self.article.pk})
        r = self.client.get(url, follow=True)

        return r
