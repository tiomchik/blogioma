from typing import Any
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request

from articles.models import Article


class ListArticleMixin(ListModelMixin):
    @method_decorator(cache_page(30))
    def list(self, request: Request) -> Any | Response:
        query = request.query_params.get("q")

        if query:
            queryset = Article.objects.filter(
                Q(heading__iregex=query) |
                Q(full_text__iregex=query) |
                Q(author__username__iregex=query)
            )
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
