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
            article = Article.objects.get(pk=pk)
            break
        except Article.DoesNotExist:
            continue

    return article
