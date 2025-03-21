from django.views.decorators.cache import cache_page
from django.urls import path

from . import views

urlpatterns = [
    path(
        "feedback/", cache_page(60 * 60)(views.Feedback.as_view()),
        name="feedback"
    ),
    path(
        "article/<int:pk>/report/",
        cache_page(60 * 60)(views.ReportArticle.as_view()),
        name="report"
    ),
]
