
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound

from api.serializers.article import ArticleSerializer
from api.utils import Pagination
from authentication.models import User
from articles.models import Article


class GetUserArticles(ListAPIView):
    serializer_class = ArticleSerializer
    filter_backends = [OrderingFilter]
    pagination_class = Pagination

    def get_queryset(self) -> list[Article]:
        username: str = self.kwargs.get("username")
        self.assert_user_exists(username)
        articles = Article.objects.filter(author__username=username)
        return articles

    def assert_user_exists(self, username: str) -> None:
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User not found.")
