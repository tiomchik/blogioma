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
        r = self._post_comment(auth=False)
        self._check_unauth_response(r)

    def test_create_without_text(self) -> None:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        r = self.client.post(url, headers=self.authorization_header)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"), ["This field is required."]
        )

    def test_create_with_very_long_text(self) -> None:
        self.comment_text = "very long comment" * 1000
        r = self._post_comment(text=self.comment_text)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"),
            ["Ensure this field has no more than 400 characters."]
        )
