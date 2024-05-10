from django.contrib.auth.models import User
from rest_framework import serializers

from articles.models import Article
from authentication.models import Profile
from comments.models import Comment
from feedback.models import Report


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "password", "last_login",
            "is_staff", "date_joined"
        )
        read_only_fields = ("last_login", "is_staff", "date_joined")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ("id", "user", "pfp")
        read_only_fields = ("id", "user", "pfp")


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    reports = serializers.HiddenField(default=None)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("author", "pub_date", "viewings", "update")


class CommentSerializer(serializers.ModelSerializer):
    # default=None because we'll link chosen article from URL in view.
    article = serializers.HiddenField(default=None)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "author", "profile", "article", "pub_date", "update"
        )


class ReportSerializer(serializers.ModelSerializer):
    # default=None the same as in CommentSerializer
    reported_article = serializers.HiddenField(default=None)

    class Meta:
        model = Report
        fields = "__all__"
