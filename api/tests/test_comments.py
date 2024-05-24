from django.urls import reverse
from django.http import HttpResponse
from rest_framework import status

from main.utils import GenericTestCase


class CommentTests(GenericTestCase):
    # ==================
    # ===== Create =====
    # ==================
    def test_create(self) -> None:
        text = "nice article"
        r = self._post_comment(text=text)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("text"), text)
        self.assertEqual(
            r.json().get("profile").get("user").get("username"),
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

    # ==================
    # ====== Read ======
    # ==================
    def test_read_list(self) -> None:
        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)

    def test_read_detail(self) -> None:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)

    def test_read_comments_of_another_article(self) -> None:
        another_article = self._create_article(headling="another article")

        url = reverse(
            "comment-list", kwargs={"article_pk": another_article.pk}
        )
        r = self.client.get(url)

        self.assertNotContains(r, self.comment.text)

    # ====================
    # ====== Update ======
    # ====================
    def test_update(self) -> None:
        text = "bad article :("
        r = self._put_comment(text=text)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("text"), text)

    def test_update_without_text(self) -> None:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.put(
            url, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"), ["This field is required."]
        )

    def test_update_with_very_long_text(self) -> None:
        text = "very looooooooooooooooooooooooooooooooooooooong comment" * 10
        r = self._put_comment(text=text)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("text"),
            ["Ensure this field has no more than 400 characters."]
        )

    def test_unauth_update(self) -> None:
        r = self._put_comment(auth=False)
        self._check_unauth_response(r)

    def test_update_nonuser_comment(self) -> None:
        another_user_data = {"username": "test_user2", "password": "12341234"}
        self._register_user(**another_user_data)
        token = self._obtain_token(**another_user_data)

        r = self._put_comment(token=token)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    # ====================
    # ====== Delete ======
    # ====================
    def test_delete(self) -> None:
        r = self._del_comment()
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauth_delete(self) -> None:
        r = self._del_comment(auth=False)
        self._check_unauth_response(r)

    def test_delete_nonuser_comment(self) -> None:
        another_user_data = {"username": "test_user3", "password": "12341234"}
        self._register_user(**another_user_data)
        token = self._obtain_token(**another_user_data)

        r = self._del_comment(token=token)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    # ========================
    # ====== Test utils ======
    # ========================
    def _post_comment(
        self, text: str = "nice article", auth: bool = True
    ) -> HttpResponse:
        """Creates a comment using POST."""
        headers = {}
        if auth:
            headers["Authorization"] = f"Token {self.token}"

        url = reverse("comment-list", kwargs={"article_pk": self.article.pk})
        data = {"text": text}
        r = self.client.post(url, data, headers=headers)

        return r

    def _put_comment(
        self, text: str = "bad article :(", auth: bool = True,
        token: str | None = None
    ) -> HttpResponse:
        """Updates a comment using PUT."""
        headers = {}
        if auth:
            headers["Authorization"] = (
                f"Token {token if token else self.token}"
            )

        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        data = {"text": text}
        r = self.client.put(url, data, headers=headers)

        return r

    def _del_comment(
        self, auth: bool = True, token: str | None = None
    ) -> HttpResponse:
        """Deletes a comment using DELETE."""
        headers = {}
        if auth:
            headers["Authorization"] = (
                f"Token {token if token else self.token}"
            )

        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.delete(url, headers=headers)

        return r
