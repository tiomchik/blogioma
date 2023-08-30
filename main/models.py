from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pfp = models.ImageField("Profile picture", upload_to="pfps/",blank=True)
    last_login = models.DateTimeField("Last login", auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return f"/profile/{self.user.username}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Article(models.Model):
    headling = models.CharField("Headling", max_length=32)
    full_text = models.TextField("Text")
    author = models.ForeignKey("Profile", models.CASCADE,
                                verbose_name="Author", unique=False)
    pub_date = models.DateTimeField("Date of publication", auto_now_add=True)
    viewings = models.IntegerField("Viewings", default=0)
    update = models.DateTimeField("Date of update", null=True, default=None)
    reports = models.IntegerField("Reports", 
                                    blank=True, null=True, default=0)

    def __str__(self):
        return f"Article: {self.headling}"

    def get_absolute_url(self):
        return f"/article/{self.pk}"

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class Comment(models.Model):
    profile = models.ForeignKey("Profile", models.CASCADE, unique=False)
    article = models.ForeignKey("Article", models.CASCADE, unique=False)
    text = models.CharField("Comment text", max_length=400,
                                                    unique=False)
    pub_date = models.DateTimeField("Date of send", auto_now_add=True)
    update = models.DateTimeField("Date of update", null=True, blank=True)

    def __str__(self):
        return f"Comment: {self.text[:20]}..."
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


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
                                verbose_name="Reason", 
                                max_length=110, choices=rules, 
                                null=False, blank=False, 
                                unique=False
                            )
    desc = models.CharField(
                                verbose_name="Description", 
                                null=True, max_length=200, 
                                blank=True, unique=False
                            )
    article = models.ForeignKey("Article", models.CASCADE, 
                                                    unique=False)
    
    def __str__(self):
        return f"{self.reason}"
    
    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
