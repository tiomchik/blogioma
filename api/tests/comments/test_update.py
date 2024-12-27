from django.urls import reverse
from rest_framework import status

from .generic import CommentsGenericTestCase


class UpdateCommentTests(CommentsGenericTestCase):
    comment_text = "bad article :("

    def test_update(self) -> None:
        r = self._put_comment(text=self.comment_text)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("text"), self.comment_text)

    def test_update_without_text(self) -> None:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.put(url, headers=self.auth_header)
        self._assert_field_is_required(r, "text")

    def test_update_with_very_long_text(self) -> None:
        self.comment_text = "very long comment" * 1000
        r = self._put_comment(text=self.comment_text)
        self._assert_field_is_too_long(r, "text")

    def test_unauth_update(self) -> None:
        self.auth_header = {}
        r = self._put_comment(text=self.comment_text)
        self._check_unauth_response(r)

    def test_update_nonuser_comment(self) -> None:
        another_user_data = {
            "username": "test_user2", 
            "password": "12341234", 
            "email": "test2@test.com"
        }
        self._register_user(**another_user_data)
        token = self._obtain_token(**another_user_data)
        self.auth_header = {"Authorization": f"Token {token}"}

        r = self._put_comment(text=self.comment_text)

        self._assert_forbidden_response(r)
