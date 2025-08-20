from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request


class ListArticleMixin(ListModelMixin):
    @method_decorator(cache_page(30))
    def list(self, request: Request) -> Response:
        return super().list(request)
