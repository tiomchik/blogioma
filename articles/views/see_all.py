from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from articles.utils import get_articles_ordered_by_field
from main.utils import get_paginator_context

order_by_options = {
    "latest": {"field": "-pub_date", "name": "Latest articles"},
    "popular": {"field": "-viewings", "name": "Popular articles \U0001F525"},
}


@cache_page(30)
def see_all(request: HttpRequest, order_by: str) -> HttpResponse:
    field = order_by_options[order_by]["field"]
    name = order_by_options[order_by]["name"]
    if order_by not in order_by_options.keys():
        raise Http404()

    articles = get_articles_ordered_by_field(field)

    context = get_paginator_context(request, articles, name)

    return render(request, "articles/see_all.html", context)
