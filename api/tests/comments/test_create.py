from django.urls import reverse
from rest_framework import status

from .generic import CommentsGenericTestCase


class CreateCommentTests(CommentsGenericTestCase):
    comment_text = "nice article"

    def test_create(self) -> None:
        r = self._post_comment(text=self.comment_text)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("text"), self.comment_text)
        self.assertEqual(
            r.json().get("profile").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        self.auth_header = {}
        r = self._post_comment(text=self.comment_text)
        self.assertUnauthResponse(r)

    def test_create_without_text(self) -> None:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        r = self.client.post(url, headers=self.auth_header)
        self.assertFieldIsRequired(r, "text")

    def test_create_with_very_long_text(self) -> None:
        self.comment_text = "very long comment" * 1000
        r = self._post_comment(text=self.comment_text)
        self.assertFieldIsTooLong(r, "text")
