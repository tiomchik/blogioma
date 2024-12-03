from typing import Any
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404

from articles.models import Article
from api.serializers import CommentSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly
from api.utils import Pagination
from comments.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by("-pub_date")
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly, )
    pagination_class = Pagination

    def perform_create(self, **kwargs) -> Comment:
        return Comment.objects.create(**kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        article = get_object_or_404(
            Article.objects.all(), pk=kwargs.get("article_pk")
        )
        comment_dict = {
            "profile": self.request.user,
            "article": article,
            "text": request.data.get("text")
        }

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_comment = self.perform_create(**comment_dict)

        headers = self.get_success_headers(serializer.data)
        return Response(
            CommentSerializer(new_comment).data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    @method_decorator(cache_page(30))
    def list(self, request: Request, *args, **kwargs) -> Any | Response:
        article_pk = kwargs.pop("article_pk")
        article = Article.objects.get(pk=article_pk)
        queryset = Comment.objects.filter(
            article=article
        ).order_by("-pub_date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, instance: Comment, new_text: str) -> Comment:
        instance.text = new_text
        instance.update = timezone.now()
        instance.save()

        return instance

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
        instance: Comment = self.get_object()
        serializer = CommentSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        new_text = request.data.get("text")
        upd_comment = self.perform_update(instance, new_text=new_text)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(CommentSerializer(upd_comment).data)
