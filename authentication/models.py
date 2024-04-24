from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pfp = models.ImageField("Profile picture", upload_to="pfps/",blank=True)
    last_login = models.DateTimeField("Last login", auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return f"/auth/profile/{self.user.username}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
