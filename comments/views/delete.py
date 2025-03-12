from django.http import (
    HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect

from articles.utils import get_article_by_pk
from comments.models import Comment


def delete_comment(
    request: HttpRequest, pk: int, comment_pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    comment = Comment.objects.get(pk=comment_pk)
    article = get_article_by_pk(pk)

    if request.user != comment.author:
        return redirect("home")
    if comment.article != article:
        return redirect("home")

    comment.delete()

    return redirect("comments", pk=pk)
