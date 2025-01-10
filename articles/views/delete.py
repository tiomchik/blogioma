from django.http import (
    HttpRequest, 
    HttpResponsePermanentRedirect,
    HttpResponseRedirect
)
from django.shortcuts import redirect

from articles.models import Article


def delete_article(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    article = Article.objects.get(pk=pk)

    if request.user == article.author or request.user.is_staff:
        article.delete()

    return redirect("home")
