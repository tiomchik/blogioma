from django import forms

from .validators import (
    linkedin_validator, tiktok_validator, twitch_validator, youtube_validator
)
from authentication.models import User


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
