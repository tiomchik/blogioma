from django.http import (
    HttpRequest, 
    HttpResponsePermanentRedirect, 
    HttpResponseRedirect
)
from django.shortcuts import redirect

from articles.utils import get_random_article


def random_article(
    request: HttpRequest
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    article = get_random_article()
    return redirect("read", pk=article.pk)
