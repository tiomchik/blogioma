from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from main.context import get_base_context


@cache_page(60 * 600)
def about(request: HttpRequest) -> HttpResponse:
    context = get_base_context(request, "About site")
    return render(request, "main/about.html", context)
