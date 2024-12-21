from django.http import HttpResponse
from django.urls import reverse

from main.utils import GenericTestCase


class CommentsGenericTestCase(GenericTestCase):
    def _post_comment(self, text: str) -> HttpResponse:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        data = {"text": text}
        r = self.client.post(url, data, headers=self.authorization_header)

        return r

    def _put_comment(self, text: str) -> HttpResponse:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        data = {"text": text}
        r = self.client.put(url, data, headers=self.authorization_header)

        return r

    def _del_comment(self) -> HttpResponse:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.delete(url, headers=self.authorization_header)

        return r
