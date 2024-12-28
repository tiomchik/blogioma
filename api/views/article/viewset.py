from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import DestroyModelMixin

from articles.models import Article
from api.serializers.article import ArticleSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly
from api.utils import Pagination
from . import (
    CreateArticleMixin,
    ListArticleMixin,
    RetrieveArticleMixin,
    UpdateArticleMixin,
    RandomArticleView
)


class ArticleViewSet(
    CreateArticleMixin,
    ListArticleMixin,
    RetrieveArticleMixin,
    UpdateArticleMixin,
    RandomArticleView,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Article.objects.order_by("-pub_date")
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly, )
    pagination_class = Pagination
