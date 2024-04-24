from django.urls import path

from . import views

urlpatterns = [
    path("", views.Search.as_view(), name="search"),
    path("<str:query>/", views.search_results, name="search_results"),
]
