from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView

from articles.models import Article
from .utils import get_base_context, DataMixin


class Home(DataMixin, ListView):
    model = Article
    template_name = "main/index.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Home")

        return dict(list(context.items()) + list(base.items()))


def about(request: HttpRequest) -> HttpResponse:
    context = get_base_context(request, "About site")

    return render(request, "main/about.html", context)
