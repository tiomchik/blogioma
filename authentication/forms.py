from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30, min_length=4, label="Username", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    email = forms.EmailField(
        max_length=320, required=False, label="Email (optional)",
        widget=forms.EmailInput(
            attrs={"class": "form-input"}
        )
    )

    password = forms.CharField(
        min_length=8, label="Password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    password1 = forms.CharField(
        min_length=8, label="Confirm password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    pfp = forms.ImageField(
        required=False, label="Profile picture (optional)",
        widget=forms.FileInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "password", "password1"]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, min_length=4, label="Username", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    password = forms.CharField(
        min_length=8, label="Password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()


class ChangeUsernameForm(forms.ModelForm):
    new_username = forms.CharField(
        max_length=30, min_length=4, label="New username",
        widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["new_username"]


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(
        min_length=8, label="New password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    new_password1 = forms.CharField(
        min_length=8, label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["new_password", "new_password1"]


class ChangePfpForm(forms.ModelForm):
    new_pfp = forms.ImageField(
        label="New profile picture", required=False, widget=forms.FileInput(
            attrs={"class": "form-input"}
        )
    )

    class Meta:
        model = User
        fields = ["new_pfp"]


# URL validators
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


class SocialMediaLinksForm(forms.ModelForm):
    youtube = forms.URLField(
        label="Youtube link", max_length=2048, required=False,
        widget=forms.URLInput(
            attrs={"class": "form-input"}
        ), validators=[youtube_validator]
    )

    tiktok = forms.URLField(
        label="TikTok link", max_length=2048, required=False,
        widget=forms.URLInput(
            attrs={"class": "form-input"}
        ), validators=[tiktok_validator]
    )

    twitch = forms.URLField(
        label="Twitch link", max_length=2048, required=False,
        widget=forms.URLInput(
            attrs={"class": "form-input"}
        ), validators=[twitch_validator]
    )

    linkedin = forms.URLField(
        label="LinkedIn link", max_length=2048, required=False,
        widget=forms.URLInput(
            attrs={"class": "form-input"}
        ), validators=[linkedin_validator]
    )

    class Meta:
        model = User
        fields = ["youtube", "tiktok", "twitch", "linkedin"]
