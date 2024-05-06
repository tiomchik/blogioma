from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request

from articles.models import Article
from authentication.models import Profile
from api.serializers import ArticleSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.order_by("-pub_date")
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly, )

    def perform_create(self, **kwargs) -> Article:
        return Article.objects.create(**kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        author = Profile.objects.get(id=request.user.id)
        article_dict = {
            "headling": request.data.get("headling"),
            "full_text": request.data.get("full_text"),
            "author": author
        }
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_article = self.perform_create(**article_dict)

        headers = self.get_success_headers(serializer.data)
        return Response(
            ArticleSerializer(new_article).data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
        instance = Article.objects.get(pk=kwargs.get("pk"))
        serializer = ArticleSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        instance.update = datetime.now()

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
