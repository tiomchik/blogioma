from comments.models import Comment

from .generic import CommentGenericTestCase


class CreateCommentTests(CommentGenericTestCase):
    text = "nice article"

    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_create(self) -> None:
        self.post_comment(text=self.text)
        self.assertCommentExists(text=self.text)

    def test_unauth_create(self) -> None:
        self.client.logout()
        self.post_comment(text=self.text)
        self.assertCommentDoesntExists(text=self.text)

    def test_create_with_blank_text(self) -> None:
        self.text = ""
        self.post_comment(text=self.text)
        self.assertCommentDoesntExists(text=self.text)

    def test_create_with_very_long_text(self) -> None:
        self.text = "nice article" * 100
        self.post_comment(text=self.text)
        self.assertCommentDoesntExists(text=self.text)
