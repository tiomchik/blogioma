from django.urls import path, include
from rest_framework import routers

from .views.article import ArticleViewSet
from .views.comment import CommentViewSet
from .views.report import ReportArticle

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"articles/(?P<article_pk>[^/.]+)/comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("articles/<int:pk>/report/", ReportArticle.as_view()),
]
