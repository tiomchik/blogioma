from django.urls import reverse

from .generic import CommentsGenericTestCase


class ReadCommentTests(CommentsGenericTestCase):
    def test_read_list(self) -> None:
        url = self.get_comment_list_url(self.article.pk)
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)

    def test_read_detail(self) -> None:
        url = reverse(
            "comment-detail",
            kwargs={"article_pk": self.article.pk, "pk": self.comment.pk}
        )
        r = self.client.get(url)

        self.assertContains(r, self.comment.text)

    def test_read_comments_of_another_article(self) -> None:
        another_article = self.create_article(heading="another article")

        url = self.get_comment_list_url(another_article.pk)
        r = self.client.get(url)

        self.assertNotContains(r, self.comment.text)

    def get_comment_list_url(self, article_pk: int) -> str:
        return reverse("comment-list", kwargs={"article_pk": article_pk})
