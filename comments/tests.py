from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase
from .models import Comment


class CommentTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()
        self.comment = Comment.objects.create(
            article=self.article, text="nice article", profile=self.user
        )

    # ==================
    # ===== Create =====
    # ==================
    def test_create(self) -> None:
        text = "nice article"
        self.post_comment(text=text)

        self.assertTrue(Comment.objects.filter(text=text).exists())

    def test_unauth_create(self) -> None:
        self.client.logout()
        text = "very nice article"
        self.post_comment(text=text)

        self.assertFalse(Comment.objects.filter(text=text).exists())

    def test_create_with_blank_text(self) -> None:
        text = ""
        self.post_comment(text=text)

        self.assertFalse(Comment.objects.filter(text=text).exists())

    def test_create_with_very_long_text(self) -> None:
        text = "nice article" * 100
        self.post_comment(text=text)

        self.assertFalse(Comment.objects.filter(text=text).exists())

    # ==================
    # ====== Read ======
    # ==================
    def test_read_list(self) -> None:
        url = reverse("comments", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)
        self.assertContains(r, self.comment.profile.username)

    def test_read_comments_of_another_article(self) -> None:
        article = self.create_article(heading="testing comments")
        self.comment.delete()
        comment = Comment.objects.create(
            article=article, text="nice article", profile=self.user
        )

        url = reverse("comments", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertNotContains(r, comment.text)

    # ====================
    # ====== Update ======
    # ====================
    def test_update(self) -> None:
        text = "bad article :("
        self.update_comment(text=text)
        self.assertTrue(Comment.objects.filter(text=text).exists())

    def test_update_with_blank_text(self) -> None:
        text = ""
        self.update_comment(text=text)
        self.assertFalse(Comment.objects.filter(text=text).exists())

    def test_update_with_very_long_text(self) -> None:
        text = "bad article :(" * 100
        self.update_comment(text=text)
        self.assertFalse(Comment.objects.filter(text=text).exists())

    def test_unauth_update(self) -> None:
        self.client.logout()
        text = "bad article :("
        self.update_comment(text=text)
        self.assertFalse(Comment.objects.filter(text=text).exists())

    def test_update_nonuser_comment(self) -> None:
        self.auth_to_another_user()
        text = "bad article :("
        self.update_comment(text=text)
        self.assertFalse(Comment.objects.filter(text=text).exists())

    # ====================
    # ====== Delete ======
    # ====================
    def test_delete(self) -> None:
        self.del_comment()
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_unauth_delete(self) -> None:
        self.client.logout()
        self.del_comment()
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_nonuser_comment(self) -> None:
        self.auth_to_another_user()
        self.del_comment()
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    # ========================
    # ====== Test utils ======
    # ========================
    def post_comment(self, text: str = "nice article") -> HttpResponse:
        """Creates a comment using POST."""
        data = urlencode({"text": text})
        url = reverse("add_comment", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        return r

    def update_comment(self, text: str = "bad article :(") -> HttpResponse:
        """Updates a comment using POST."""
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

    def del_comment(self) -> HttpResponse:
        """Deletes a comment using GET."""
        url = reverse(
            "delete_comment",
            kwargs={"pk": self.article.pk, "comment_pk": self.comment.pk}
        )
        r = self.client.get(url)

        return r
