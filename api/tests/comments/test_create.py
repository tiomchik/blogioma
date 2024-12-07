from django.urls import reverse
from rest_framework import status

from .generic import CommentsGenericTestCase


class CreateCommentTests(CommentsGenericTestCase):
    def test_create(self) -> None:
        text = "nice article"
        r = self._post_comment(text=text)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("text"), text)
        self.assertEqual(
            r.json().get("profile").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        r = self._post_comment(auth=False)
        self._check_unauth_response(r)

    def test_create_without_text(self) -> None:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        r = self.client.post(
            url, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"), ["This field is required."]
        )

    def test_create_with_very_long_text(self) -> None:
        text = "very looooooooooooooooooooooooooooooooooooooong comment" * 10
        r = self._post_comment(text=text)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"),
            ["Ensure this field has no more than 400 characters."]
        )
