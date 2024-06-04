from django.db import models

from authentication.models import Profile


class Article(models.Model):
    headling = models.CharField("Headling", max_length=100)
    full_text = models.TextField("Text")
    author = models.ForeignKey(
        Profile, models.CASCADE,verbose_name="Author",
        unique=False
    )
    pub_date = models.DateTimeField("Date of publication", auto_now_add=True)
    viewings = models.IntegerField("Viewings", default=0)
    update = models.DateTimeField("Date of update", null=True, default=None)
    reports = models.ManyToManyField("feedback.Report", blank=True)

    def __str__(self) -> str:
        return f"Article: {self.headling}"

    def get_absolute_url(self) -> str:
        return f"/article/{self.pk}"

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"
