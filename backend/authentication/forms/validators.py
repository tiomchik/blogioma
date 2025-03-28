from django.forms import ValidationError


def url_platform_validator(
    value: str, platform: str, platform_url_part: str
) -> None:
    if value != "" and platform_url_part not in value:
        raise ValidationError(f"This is not a {platform.capitalize()} link.")


def youtube_validator(value: str) -> None:
    url_platform_validator(value, "YouTube", "youtube.com/")


def tiktok_validator(value: str) -> None:
    url_platform_validator(value, "TikTok", "tiktok.com/")


def twitch_validator(value: str) -> None:
    url_platform_validator(value, "Twitch", "twitch.tv/")


def linkedin_validator(value: str) -> None:
    url_platform_validator(value, "LinkedIn", "linkedin.com/")
