from django.urls import path, include
from rest_framework import routers

from .views.article import ArticleViewSet

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
