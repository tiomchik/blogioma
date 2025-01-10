from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from articles.models import Article
from main.utils import get_paginator_context


@cache_page(30)
def see_all(request: HttpRequest, order_by: str) -> HttpResponse:
    if order_by == "latest":
        field = "-pub_date"
        name = "Latest articles"
    elif order_by == "popular":
        field = "-viewings"
        name = "Popular articles \U0001F525"
    else:
        raise Http404()

    articles = Article.objects.order_by(field).values(
        "heading", "full_text", "update", "pub_date", "pk", 
        "author", "author__pfp", "author__username"
    )

    context = get_paginator_context(request, articles, name)

    return render(request, "articles/see_all.html", context)
