from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
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

    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = (
            "id", "username", "password", "last_login",
            "is_staff", "date_joined", "email", "pfp",
            "youtube", "tiktok", "twitch", "linkedin"
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


class EditUserSerializer(UserSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
