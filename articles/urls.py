from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path(
        "add_article/", cache_page(60 * 60)(views.AddArticle.as_view()),
        name="add_article"
    ),
    path(
        "article/<int:pk>/", cache_page(60 * 60)(views.ReadArticle.as_view()),
        name="read"
    ),
    path("article/<int:pk>/delete/", views.delete_article, name="delete"),
    path(
        "article/<int:pk>/update/",
        cache_page(60 * 60)(views.UpdateArticle.as_view()),
        name="update"
    ),
    path("article/random/", views.random_article, name="random_article"),
    path("article/<str:order_by>/", views.see_all, name="see_all"),
]
