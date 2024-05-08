from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views.article import ArticleViewSet
from .views.comment import CommentViewSet
from .views.report import ReportArticle
from .views.authentication import RegisterView

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"articles/(?P<article_pk>[^/.]+)/comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("articles/<int:pk>/report/", ReportArticle.as_view()),

    # Authentication
    path("auth/obtain-token/", views.obtain_auth_token),
    path("auth/register/", RegisterView.as_view()),
]
