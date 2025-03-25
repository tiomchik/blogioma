from typing import Any
from django.views.generic.list import ListView

from articles.models import Article
from main.mixins import DataMixin


class Home(DataMixin, ListView):
    model = Article
    template_name = "main/index.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Home")

        return dict(list(context.items()) + list(base.items()))
