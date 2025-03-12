from comments.models import Comment

from .generic import CommentGenericTestCase


class UpdateCommentTests(CommentGenericTestCase):
    text = "bad article :("

    def test_update(self) -> None:
        self.update_comment(text=self.text)
        self.assertTrue(Comment.objects.filter(text=self.text).exists())

    def test_update_with_blank_text(self) -> None:
        self.text = ""
        self.update_comment(text=self.text)
        self.assertFalse(Comment.objects.filter(text=self.text).exists())

    def test_update_with_very_long_text(self) -> None:
        self.text = "bad article :(" * 100
        self.update_comment(text=self.text)
        self.assertFalse(Comment.objects.filter(text=self.text).exists())

    def test_unauth_update(self) -> None:
        self.client.logout()
        self.update_comment(text=self.text)
        self.assertFalse(Comment.objects.filter(text=self.text).exists())

    def test_update_nonuser_comment(self) -> None:
        self.auth_to_another_user()
        self.update_comment(text=self.text)
        self.assertFalse(Comment.objects.filter(text=self.text).exists())
