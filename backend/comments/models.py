from django.db import models

from articles.models import Article
from authentication.models import User


class Comment(models.Model):
    author = models.ForeignKey(User, models.CASCADE, unique=False)
    article = models.ForeignKey(Article, models.CASCADE, unique=False)
    text = models.CharField("Comment text", max_length=400, unique=False)
    pub_date = models.DateTimeField("Date of send", auto_now_add=True)
    update = models.DateTimeField("Date of update", null=True, blank=True)

    def __str__(self) -> str:
        return f"Comment: {self.text[:20]}..."

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
