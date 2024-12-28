from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request

from articles.utils import search_articles


class ListArticleMixin(ListModelMixin):
    @method_decorator(cache_page(30))
    def list(self, request: Request) -> Response:
        query = request.query_params.get("q")

        if query:
            queryset = search_articles(query)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
