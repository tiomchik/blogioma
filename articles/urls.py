from django.views.decorators.cache import cache_page

from main.utils import my_path
from . import views

urlpatterns = [
    my_path(
        "article/<int:pk>/", cache_page(60 * 60)(views.ReadArticle.as_view()),
        name="read"
    ),
    my_path("article/random/", views.random_article, name="random_article"),
    my_path("article/<str:order_by>/", views.see_all, name="see_all"),
    my_path(
        "add_article/", cache_page(60 * 60)(views.AddArticle.as_view()),
        name="add_article"
    ),
    my_path("article/<int:pk>/delete/", views.delete_article, name="delete"),
    my_path(
        "article/<int:pk>/update/",
        cache_page(60 * 60)(views.UpdateArticle.as_view()),
        name="update"
    ),
]
