from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin

from articles.models import Article
from api.serializers import ArticleSerializer


class UpdateArticleMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
        instance: Article = self.get_object()
        serializer = ArticleSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        instance.update = timezone.now()

        # In serializer.save() occures TypeError: "'NoneType' object
        # is not iterable", but the update is successful.
        # That's why we need to wrap this method in try/except.
        try:
            serializer.save()
        except TypeError:
            pass

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
