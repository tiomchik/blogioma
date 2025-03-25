from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from articles.models import Article
from authentication.models import User
from main.context import get_page_obj


@cache_page(30)
def profile(request: HttpRequest, username: str) -> HttpResponse:
    articles = get_articles_by_authors_name(username)
    context = {
        "name": f"{username}'s profile",
        "profile": get_object_or_404(User, username=username),
        "page_obj": get_page_obj(request, articles)
    }
    return render(request, "profile/profile.html", context)


def get_articles_by_authors_name(
    author_name: str
) -> list[Article]:
    return Article.objects.filter(author__username=author_name).values(
        "heading", "full_text", "update", 
        "pub_date", "pk", "author",
        "author__pfp", "author__username"
    )
