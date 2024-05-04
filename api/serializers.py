from rest_framework import serializers

from articles.models import Article
from comments.models import Comment
from feedback.models import Report


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CurrentUserDefault()
    reports = serializers.HiddenField(default=None)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("author", "pub_date", "viewings", "update")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    # default=None because we'll link chosen article from URL in
    # ReportArticle view.
    reported_article = serializers.HiddenField(default=None)

    class Meta:
        model = Report
        fields = "__all__"
