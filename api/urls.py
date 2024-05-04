from django.urls import path, include
from rest_framework import routers

from .views.article import ArticleViewSet
from .views.report import ReportArticle

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("articles/<int:pk>/report/", ReportArticle.as_view()),
]
