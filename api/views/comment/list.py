from typing import Any
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from articles.models import Article
from comments.models import Comment


class ListCommentMixin(ListModelMixin):
    @method_decorator(cache_page(30))
    def list(self, request: Request, **kwargs) -> Any | Response:
        article_pk = kwargs.pop("article_pk")
        article = Article.objects.get(pk=article_pk)
        queryset = Comment.objects.filter(
            article=article
        ).order_by("-pub_date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
