from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from articles.utils import get_article_by_pk
from articles.models import Article
from main.paginator import get_page_obj
from comments.models import Comment


@cache_page(30)
def get_comments(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_article_by_pk(pk)
    comments = get_comments_by_article(article)
    context = {
        "name": f"Comments to article \"{article.heading}\".",
        "page_obj": get_page_obj(request, comments),
        "article": article
    }
    return render(request, "comments/comments.html", context)


def get_comments_by_article(article: Article) -> list[Comment]:
    return Comment.objects.filter(article=article).values(
        "author", "author__pfp", "pk", "article__pk",
        "author__username", "update", "pub_date", "text"
    )
