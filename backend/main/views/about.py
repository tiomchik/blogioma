from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 600)
def about(request: HttpRequest) -> HttpResponse:
    context = {"name": "About site"}
    return render(request, "main/about.html", context)
