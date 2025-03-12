from django.urls import reverse
from comments.models import Comment

from .generic import CommentGenericTestCase


class ReadCommentTests(CommentGenericTestCase):
    def test_read_list(self) -> None:
        url = reverse("comments", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)
        self.assertContains(r, self.comment.author.username)

    def test_read_comments_of_another_article(self) -> None:
        article = self.create_article(heading="testing comments")
        self.comment.delete()
        comment = Comment.objects.create(
            article=article, text="nice article", author=self.user
        )

        url = reverse("comments", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertNotContains(r, comment.text)
