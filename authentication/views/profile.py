from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from articles.models import Article
from authentication.models import User
from main.utils import get_paginator_context


@cache_page(30)
def profile(request: HttpRequest, username: str) -> HttpResponse:
    articles = Article.objects.filter(author__username=username).values(
        "heading", "full_text", "update", 
        "pub_date", "pk", "author", "author__pfp", 
        "author__username"
    )

    context = get_paginator_context(
        request, articles, f"{username}'s profile",
        profile=get_object_or_404(User, username=username)
    )

    return render(request, "profile/profile.html", context)
