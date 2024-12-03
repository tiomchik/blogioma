from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("Email address", null=True, blank=True)
    pfp = models.ImageField("Profile picture", upload_to="pfps/",blank=True)
    last_login = models.DateTimeField("Last login", auto_now=True)
    youtube = models.CharField(
        "Youtube link", max_length=2048, blank=True, null=True
    )
    tiktok = models.CharField(
        "TikTok link", max_length=2048, blank=True, null=True
    )
    twitch = models.CharField(
        "Twitch link", max_length=2048, blank=True, null=True
    )
    linkedin = models.CharField(
        "LinkedIn link", max_length=2048, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.username}"

    def get_absolute_url(self) -> str:
        return f"/auth/profile/{self.username}"
