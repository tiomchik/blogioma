from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from typing import Any
from random import randint
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request

from articles.models import Article
from authentication.models import User
from api.serializers import ArticleSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly
from api.utils import Pagination, plus_viewing


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.order_by("-pub_date")
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly, )
    pagination_class = Pagination

    def perform_create(self, **kwargs) -> Article:
        return Article.objects.create(**kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        article_dict = {
            "headling": request.data.get("headling"),
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

    @method_decorator(cache_page(30))
    def list(self, request: Request, *args, **kwargs) -> Any | Response:
        query = request.query_params.get("q")

        # If search query passed, then select articles that matches this query
        if query:
            queryset = Article.objects.filter(
                # By headling
                Q(headling__iregex=query) | 
                # Full text
                Q(full_text__iregex=query) |
                # Author username
                Q(author__username__iregex=query)
            )
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(30))
    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        plus_viewing(instance)
        serializer = ArticleSerializer(instance)
        return Response(serializer.data)

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
