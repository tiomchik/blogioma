from django.urls import path

from . import views

urlpatterns = [
    path("add_article/", views.AddArticle.as_view(), name="add_article"),
    path("article/<int:pk>/", views.ReadArticle.as_view(), name="read"),
    path("article/<int:pk>/delete/", views.delete_article, name="delete"),
    path(
        "article/<int:pk>/update/", views.UpdateArticle.as_view(),
        name="update"
    ),
    path("article/random/", views.random_article, name="random_article"),
    path("article/<str:order_by>/", views.see_all, name="see_all"),
]