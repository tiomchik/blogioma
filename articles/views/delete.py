from django.http import (
    HttpRequest, 
    HttpResponsePermanentRedirect,
    HttpResponseRedirect
)
from django.shortcuts import redirect

from articles.models import Article
from articles.utils import get_article_by_pk
from authentication.models import User


def delete_article(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    article = get_article_by_pk(pk)

    if is_author_or_staff(request.user, article):
        article.delete()

    return redirect("home")


def is_author_or_staff(user: User, article: Article) -> bool:
    return user == article.author or user.is_staff
