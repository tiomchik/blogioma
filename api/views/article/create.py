from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import CreateModelMixin

from articles.models import Article
from api.serializers import ArticleSerializer


class CreateArticleMixin(CreateModelMixin):
    def perform_create(self, **kwargs) -> Article:
        return Article.objects.create(**kwargs)

    def create(self, request: Request) -> Response:
        article_dict = {
            "heading": request.data.get("heading"),
            "full_text": request.data.get("full_text"),
            "author": self.request.user
        }
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_article = self.perform_create(**article_dict)

        headers = self.get_success_headers(serializer.data)
        return Response(
            ArticleSerializer(new_article).data,
            status=status.HTTP_201_CREATED, headers=headers
        )
