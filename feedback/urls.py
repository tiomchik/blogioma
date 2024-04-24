from django.urls import path

from . import views

urlpatterns = [
    path("feedback/", views.Feedback.as_view(), name="feedback"),
    path(
        "article/<int:pk>/report/", views.ReportArticle.as_view(),
        name="report"
    ),
]
