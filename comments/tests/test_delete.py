from .generic import CommentGenericTestCase


class DeleteCommentTests(CommentGenericTestCase):
    def test_delete(self) -> None:
        self.delete_comment()
        self.assertCommentDoesntExists(pk=self.comment.pk)

    def test_unauth_delete(self) -> None:
        self.client.logout()
        self.delete_comment()
        self.assertCommentExists(pk=self.comment.pk)

    def test_delete_nonuser_comment(self) -> None:
        self.auth_to_another_user()
        self.delete_comment()
        self.assertCommentExists(pk=self.comment.pk)
