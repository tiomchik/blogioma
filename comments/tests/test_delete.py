from comments.models import Comment

from .generic import CommentGenericTestCase


class DeleteCommentTests(CommentGenericTestCase):
    def test_delete(self) -> None:
        self.delete_comment()
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_unauth_delete(self) -> None:
        self.client.logout()
        self.delete_comment()
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_nonuser_comment(self) -> None:
        self.auth_to_another_user()
        self.delete_comment()
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
