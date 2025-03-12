from django.http import (
    HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect

from authentication.models import User
from articles.utils import get_article_by_pk
from comments.models import Comment


def delete_comment(
    request: HttpRequest, pk: int, comment_pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    comment = Comment.objects.get(pk=comment_pk)
    article = get_article_by_pk(pk)

    if not is_author_or_staff(request.user, article):
        return redirect("home")
    if comment.article != article:
        return redirect("home")

    comment.delete()

    return redirect("comments", pk=pk)


def is_author_or_staff(user: User, comment: Comment):
    return user == comment.author or user.is_staff
