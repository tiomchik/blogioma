from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from articles.utils import search_articles


class SearchArticlesView(ListAPIView):
    @action(
        methods=["get"], detail=False, url_path="search",
        url_name="search-articles"
    )
    def get(self, request: Request) -> Response:
        query = request.query_params.get("q", "")
        queryset = search_articles(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
