from django.utils import timezone
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.comment import CommentSerializer
from comments.models import Comment


class UpdateCommentMixin(UpdateModelMixin):
    def update(self, request: Request, **kwargs) -> Response:
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

    def perform_update(self, instance: Comment, new_text: str) -> Comment:
        instance.text = new_text
        instance.update = timezone.now()
        instance.save()

        return instance
