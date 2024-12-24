from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from articles.models import Article
from api.serializers import CommentSerializer
from comments.models import Comment


class CreateCommentMixin(CreateModelMixin):
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
