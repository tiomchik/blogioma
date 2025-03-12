from comments.models import Comment

from .generic import CommentGenericTestCase


class UpdateCommentTests(CommentGenericTestCase):
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
