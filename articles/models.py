from django.db import models

from authentication.models import Profile


class Article(models.Model):
    headling = models.CharField("Headling", max_length=32)
    full_text = models.TextField("Text")
    author = models.ForeignKey(
        Profile, models.CASCADE,verbose_name="Author",
        unique=False
    )
    pub_date = models.DateTimeField("Date of publication", auto_now_add=True)
    viewings = models.IntegerField("Viewings", default=0)
    update = models.DateTimeField("Date of update", null=True, default=None)
    reports = models.IntegerField("Reports", blank=True, null=True, default=0)

    def __str__(self):
        return f"Article: {self.headling}"

    def get_absolute_url(self):
        return f"/article/{self.pk}"

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
