from django.http import HttpResponse
from django.urls import reverse

from main.generic_test_cases import APIGenericTestCase


class CommentsGenericTestCase(APIGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()
        self.comment = self.create_comment(article=self.article)

    def post_comment(self, text: str) -> HttpResponse:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        data = {"text": text}
        r = self.client.post(url, data, headers=self.auth_header)

        return r

    def put_comment(self, text: str) -> HttpResponse:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        data = {"text": text}
        r = self.client.put(url, data, headers=self.auth_header)

        return r

    def del_comment(self) -> HttpResponse:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.delete(url, headers=self.auth_header)

        return r
