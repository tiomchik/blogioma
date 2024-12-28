from rest_framework import routers

from .views.article.viewset import ArticleViewSet
from .views.comment.viewset import CommentViewSet

router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"articles/(?P<article_pk>[^/.]+)/comments", CommentViewSet)
