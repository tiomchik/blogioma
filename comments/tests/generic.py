from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from comments.models import Comment
from main.utils import GenericTestCase


class CommentGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()
        self.comment = Comment.objects.create(
            article=self.article, text="nice article", author=self.user
        )

    def post_comment(self, text: str) -> HttpResponse:
        data = urlencode({"text": text})
        url = reverse("add_comment", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        return r

    def get_comments(self) -> HttpResponse:
        url = reverse("comments", kwargs={"pk": self.article.pk})
        r = self.client.get(url)
        return r

    def update_comment(self, text: str) -> HttpResponse:
        data = urlencode({"text": text})
        url = reverse(
            "update_comment",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        return r

    def delete_comment(self) -> HttpResponse:
        url = reverse(
            "delete_comment",
            kwargs={"pk": self.article.pk, "comment_pk": self.comment.pk}
        )
        r = self.client.get(url)

        return r
