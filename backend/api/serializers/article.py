from rest_framework import serializers

from .user import UserSerializer
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reports = serializers.HiddenField(default=None)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("author", "pub_date", "viewings", "update")
