from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.utils import get_random_article
from api.serializers.article import ArticleSerializer


class RandomArticleView(APIView):
    @action(
        methods=["get"], detail=False, url_path="random",
        url_name="random-article"
    )
    def random_article(self, request: Request) -> Response:
        article = get_random_article()
        article.increment_viewings()
        article.save_and_refresh()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
