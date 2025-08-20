from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class SearchArticlesView(ListAPIView):
    search_fields = ["heading", "full_text", "author__username"]

    @action(
        methods=["get"], detail=False, url_path="search",
        url_name="search-articles"
    )
    def get(self, request: Request) -> Response:
        return super().list(request)
