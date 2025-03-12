from comments.models import Comment

from .generic import CommentGenericTestCase


class CreateCommentTests(CommentGenericTestCase):
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