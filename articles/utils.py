from django.db.models import Q
from random import randint

from .models import Article


def search_articles(query: str) -> list[Article]:
    return Article.objects.filter(
        Q(heading__iregex=query) |
        Q(full_text__iregex=query) |
        Q(author__username__iregex=query)
    )


def get_random_article() -> Article:
    total = Article.objects.last().pk

    article = None
    while True:
        pk = randint(0, total)

        try:
            article = get_article_by_pk(pk)
            break
        except Article.DoesNotExist:
            continue

    return article


def get_article_by_pk(pk: int) -> Article:
    return Article.objects.get(pk=pk)


def get_articles_ordered_by_field(field: str) -> list[Article]:
    return Article.objects.order_by(field).values(
        "heading", "full_text", "update", "pub_date", "pk",
        "author", "author__pfp", "author__username"
    )
