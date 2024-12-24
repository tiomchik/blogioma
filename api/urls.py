from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework.authtoken import views

from main.utils import my_path
from .views.article.viewset import ArticleViewSet
from .views.comment import CommentViewSet
from .views.report import ReportArticle
from .views.authentication import RegisterView, Me, Edit

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"articles/(?P<article_pk>[^/.]+)/comments", CommentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Blogioma API",
        default_version="v1",
        description="Simple Django blog application (https://github.com/tiomchik/blogioma)",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    my_path("", include(router.urls)),

    my_path("auth/obtain-token/", views.obtain_auth_token, name="obtain-token"),
    my_path("auth/register/", RegisterView.as_view(), name="register"),
    my_path("auth/me/", Me.as_view(), name="me"),
    my_path("auth/me/edit/", Edit.as_view(), name="edit-me"),

    my_path(
        "articles/<int:pk>/report/", ReportArticle.as_view(),
        name="report-article"
    ),

    my_path(
        "docs/", schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
]
