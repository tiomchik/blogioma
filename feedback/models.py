from django.db import models

from articles.models import Article
from authentication.models import User

rules = (
    ("Banned advertising", 
        "Banned advertising (casino, porn-sites, etc.)"),
    ("Banned content", 
        "Content that is unpleasant to some readers (shock content, etc.), illegal or tragic content"),
    ("18+ content", "18+ content"),
    ("Scam", "Scam"),
    ("Swearing", "Swearing"),
    ("Copyright infringement", "Copyright infringement"),
    ("Data/media leakage", 
        "Data/media leakage (paid courses, candid photos, etc.)"),
)


class Report(models.Model):
    reason = models.CharField(
        verbose_name="Reason", max_length=110, choices=rules,
        null=False, blank=False, unique=False
    )
    desc = models.CharField(
        verbose_name="Description", null=True, max_length=200, 
        blank=True, unique=False
    )
    reported_article = models.ForeignKey(
        Article, on_delete=models.CASCADE, unique=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)

    def __str__(self) -> str:
        return f"{self.reason}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
