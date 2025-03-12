from django.urls import reverse
from comments.models import Comment

from .generic import CommentGenericTestCase


class ReadCommentTests(CommentGenericTestCase):
    def test_read_list(self) -> None:
        r = self.get_comments()
        self.assertContains(r, self.comment.text)
        self.assertContains(r, self.comment.author.username)

    def test_read_comments_of_another_article(self) -> None:
        article = self.create_article(heading="testing comments")
        self.comment.delete()
        comment = Comment.objects.create(
            article=article, text="nice article", author=self.user
        )

        r = self.get_comments()

        self.assertNotContains(r, comment.text)
