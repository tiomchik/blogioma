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


def url_platform_validator(
    value: str, platform: str, platform_url_part: str
) -> None:
    if value != "" and platform_url_part not in value:
        raise serializers.ValidationError(
            f"This is not a {platform.capitalize()} link."
        )

    return value


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    youtube = serializers.CharField(allow_blank=True, required=False)
    tiktok = serializers.CharField(allow_blank=True, required=False)
    twitch = serializers.CharField(allow_blank=True, required=False)
    linkedin = serializers.CharField(allow_blank=True, required=False)

    def validate_youtube(self, value: str) -> str:
        return url_platform_validator(value, "YouTube", "youtube.com/")

    def validate_tiktok(self, value: str) -> str:
        return url_platform_validator(value, "TikTok", "tiktok.com/")

    def validate_twitch(self, value: str) -> str:
        return url_platform_validator(value, "Twitch", "twitch.tv/")

    def validate_linkedin(self, value: str) -> str:
        return url_platform_validator(value, "LinkedIn", "linkedin.com/")

    class Meta:
        model = Profile
        fields = (
            "id", "user", "pfp", "youtube", "tiktok", "twitch", "linkedin"
        )
        read_only_fields = ("id", "pfp")


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
    owner = ProfileSerializer(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
