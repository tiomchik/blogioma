from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from articles.utils import search_articles
from main.context import get_paginator_context


def search_results(request: HttpRequest, query: str) -> HttpResponse:
    articles = search_articles(query).values(
        "heading", "full_text", "update", "pub_date", "pk",
        "author", "author__pfp", "author__username"
    )

    context = get_paginator_context(
        request, articles, f"Search results by query: \"{query}\"",
        on_search_page=1
    )

    return render(request, "search/search_results.html", context)
