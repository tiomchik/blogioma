from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from comments.models import Comment
from main.generic_test_cases import SessionAuthGenericTestCase


class CommentGenericTestCase(SessionAuthGenericTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.article = self.create_article()
        self.comment = self.create_comment(article=self.article)

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

    def assertCommentExists(self, **filter_kwargs) -> None:
        self.assertTrue(Comment.objects.filter(**filter_kwargs).exists())

    def assertCommentDoesntExists(self, **filter_kwargs) -> None:
        self.assertFalse(Comment.objects.filter(**filter_kwargs).exists())

    def assertPageContainsComment(self, r: HttpResponse) -> None:
        self.assertContains(r, self.comment.text)
        self.assertContains(r, self.comment.author.username)
