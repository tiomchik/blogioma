from rest_framework import serializers

from .user import UserSerializer
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.HiddenField(default=None)
    profile = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "author", "profile", "article", "pub_date", "update"
        )