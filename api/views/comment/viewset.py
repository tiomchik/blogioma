from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CommentSerializer
from api.permissions import IsAuthorOrStaffOrReadOnly
from api.utils import Pagination
from comments.models import Comment
from . import CreateCommentMixin, ListCommentMixin, UpdateCommentMixin


class CommentViewSet(
    CreateCommentMixin,
    ListCommentMixin,
    UpdateCommentMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Comment.objects.order_by("-pub_date")
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly, )
    pagination_class = Pagination
