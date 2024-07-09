from django.views.decorators.cache import cache_page

from main.utils import my_path
from . import views

urlpatterns = [
    my_path(
        "article/<int:pk>/comments/", views.see_comments, name="comments"
    ),
    my_path(
        "article/<int:pk>/add_comment/",
        cache_page(60 * 60)(views.AddComment.as_view()), name="add_comment"
    ),
    my_path(
        "article/<int:pk>/comments/<int:comment_pk>/delete",
        views.delete_comment, name="delete_comment"
    ),
    my_path(
        "article/<int:article_pk>/comments/<int:pk>/update",
        cache_page(60 * 60)(views.UpdateComment.as_view()),
        name="update_comment"
    ),
]
