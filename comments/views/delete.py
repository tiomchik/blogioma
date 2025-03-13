from django.http import (
    HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect

from authentication.models import User
from articles.utils import get_article_by_pk
from articles.models import Article
from comments.models import Comment


def delete_comment(
    request: HttpRequest, pk: int, comment_pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    comment = Comment.objects.get(pk=comment_pk)
    article = get_article_by_pk(pk)

    if is_comment_can_be_deleted(request.user, comment, article):
        comment.delete()

    return redirect("comments", pk=pk)


def is_comment_can_be_deleted(
    user: User, comment: Comment, article: Article
) -> bool:
    return is_author_or_staff(user, comment) and is_article_comment(
        comment, article
    )


def is_author_or_staff(user: User, comment: Comment) -> bool:
    return user == comment.author or user.is_staff


def is_article_comment(comment: Comment, article: Article) -> bool:
    return comment.article == article
