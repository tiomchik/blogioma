from django.db.models import Q

from .models import Article


def search_articles(query: str) -> list[Article]:
    return Article.objects.filter(
        Q(heading__iregex=query) |
        Q(full_text__iregex=query) |
        Q(author__username__iregex=query)
    )
