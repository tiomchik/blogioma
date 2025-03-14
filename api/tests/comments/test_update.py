from django.urls import reverse

from .generic import CommentsGenericTestCase


class UpdateCommentTests(CommentsGenericTestCase):
    comment_text = "bad article :("

    def test_update(self) -> None:
        r = self.put_comment(text=self.comment_text)
        self.assertOkStatus(r)
        self.assertEqual(r.json().get("text"), self.comment_text)

    def test_update_without_text(self) -> None:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.put(url, headers=self.auth_header)
        self.assertFieldIsRequiredInJson(r, "text")

    def test_update_with_very_long_text(self) -> None:
        self.comment_text = "very long comment" * 1000
        r = self.put_comment(text=self.comment_text)
        self.assertFieldIsTooLong(r, "text")

    def test_unauth_update(self) -> None:
        self.auth_header = {}
        r = self.put_comment(text=self.comment_text)
        self.assertUnauthResponse(r)

    def test_update_nonuser_comment(self) -> None:
        another_user_data = {
            "username": "test_user2", 
            "password": "12341234", 
            "email": "test2@test.com"
        }
        self._set_another_user(**another_user_data)
        r = self.put_comment(text=self.comment_text)
        self.assertForbiddenResponse(r)
