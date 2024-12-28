from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin

from articles.models import Article
from api.serializers.article import ArticleSerializer


class RetrieveArticleMixin(RetrieveModelMixin):
    @method_decorator(cache_page(30))
    def retrieve(self, request: Request, **kwargs) -> Response:
        instance: Article = self.get_object()
        instance.increment_viewings()
        instance.save_and_refresh()
        serializer = ArticleSerializer(instance)
        return Response(serializer.data)
