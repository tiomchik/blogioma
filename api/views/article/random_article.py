from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint

from articles.models import Article
from api.utils import plus_viewing
from api.serializers import ArticleSerializer


class RandomArticleView(APIView):
    @action(
        methods=["get"], detail=False, url_path="random",
        url_name="random-article"
    )
    def random_article(self, request: Request) -> Response:
        total = Article.objects.last().pk

        article = None
        while True:
            pk = randint(0, total)

            try:
                article = Article.objects.get(pk=pk)
                break
            except Article.DoesNotExist:
                continue

        plus_viewing(article)

        serializer = ArticleSerializer(article)
        return Response(serializer.data)
