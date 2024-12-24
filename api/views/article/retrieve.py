from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin

from api.utils import plus_viewing
from api.serializers import ArticleSerializer


class RetrieveArticleMixin(RetrieveModelMixin):
    @method_decorator(cache_page(30))
    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        plus_viewing(instance)
        serializer = ArticleSerializer(instance)
        return Response(serializer.data)
