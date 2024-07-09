from django.views.decorators.cache import cache_page

from main.utils import my_path
from . import views

urlpatterns = [
    my_path(
        "feedback/", cache_page(60 * 60)(views.Feedback.as_view()),
        name="feedback"
    ),
    my_path(
        "article/<int:pk>/report/",
        cache_page(60 * 60)(views.ReportArticle.as_view()),
        name="report"
    ),
]
