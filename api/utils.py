from django.db.models import F
from rest_framework.pagination import PageNumberPagination

from articles.models import Article


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


def plus_viewing(article: Article) -> None:
    article.viewings = F("viewings") + 1
    article.save()
    article.refresh_from_db()
