from django.urls import include, path
from rest_framework.authtoken import views

from .router import router
from .swagger import schema_view
from .views.report import ReportArticle
from .views.feedback import Feedback
from .views.authentication import RegisterView, Me, Edit
from .views.user.retrieve import RetrieveUserView

urlpatterns = [
    path("", include(router.urls)),

    path("auth/obtain-token/", views.obtain_auth_token, name="obtain-token"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", Me.as_view(), name="me"),
    path("auth/me/edit/", Edit.as_view(), name="edit-me"),

    path("users/<str:username>/", RetrieveUserView.as_view(), name="user-detail"),

    path(
        "articles/<int:pk>/report/", ReportArticle.as_view(),
        name="report-article"
    ),
    path("feedback/", Feedback.as_view(), name="feedback-api"),

    path(
        "docs/", schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
]
