from django.urls import include
from rest_framework.authtoken import views

from .router import router
from .swagger import schema_view
from .views.report import ReportArticle
from .views.authentication import RegisterView, Me, Edit
from main.utils import my_path

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
