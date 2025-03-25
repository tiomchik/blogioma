from typing import Any
from django.views.generic.detail import DetailView

from main.mixins import DataMixin
from articles.models import Article


class ReadArticle(DataMixin, DetailView):
    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        article: Article = context["article"]
        article.increment_viewings()
        article.save_and_refresh()

        context["name"] = article.heading
        context["article"] = article
        return context
