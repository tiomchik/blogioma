from comments.models import Comment

from .generic import CommentGenericTestCase


class ReadCommentTests(CommentGenericTestCase):
    def test_read_list(self) -> None:
        r = self.get_comments()
        self.assertPageContainsComment(r)

    def test_read_comments_of_another_article(self) -> None:
        article = self.create_article(heading="testing comments")
        self.comment.delete()
        comment = Comment.objects.create(
            article=article, text="nice article", author=self.user
        )

        r = self.get_comments()
        self.assertNotContains(r, comment.text)
