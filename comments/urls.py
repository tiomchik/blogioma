from django.urls import path

from . import views

urlpatterns = [
    path("article/<int:pk>/comments/", views.see_comments, name="comments"),
    path(
        "article/<int:pk>/add_comment/", views.AddComment.as_view(),
        name="add_comment"
    ),
    path(
        "article/<int:pk>/comments/<int:comment_pk>/delete",
        views.delete_comment, name="delete_comment"
    ),
    path(
        "article/<int:article_pk>/comments/<int:pk>/update",
        views.UpdateComment.as_view(), name="update_comment"
    ),
]
