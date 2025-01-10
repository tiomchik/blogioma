from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.utils import timezone

from articles.models import Article
from articles.forms import AddArticleForm
from main.utils import DataMixin


class UpdateArticle(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "articles/update_article.html"
    form_class = AddArticleForm
    model = Article

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Update article")
        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: AddArticleForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        article = get_object_or_404(Article, pk=self.kwargs["pk"])
        self.update_and_save(article, form.cleaned_data)
        return redirect("read", pk=self.kwargs["pk"])

    def update_and_save(self, article: Article, data: dict[str]) -> None:
        article.update = timezone.now()
        article.heading = data.get("heading")
        article.full_text = data.get("full_text")
        article.save()
