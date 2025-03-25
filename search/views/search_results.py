from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from articles.utils import search_articles
from main.context import get_page_obj


def search_results(request: HttpRequest, query: str) -> HttpResponse:
    articles = search_articles(query).values(
        "heading", "full_text", "update", "pub_date", "pk",
        "author", "author__pfp", "author__username"
    )
    context = {
        "name": f"Search results by query: \"{query}\"",
        "page_obj": get_page_obj(request, articles),
        "illuminate_search_button": True
    }
    return render(request, "search/search_results.html", context)
