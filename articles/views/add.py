from typing import Any
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from articles.models import Article
from articles.forms import AddArticleForm
from main.mixins import DataMixin


class AddArticle(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = "articles/add_article.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Add Article"
        # on_add_article_page for illumination of add article button
        context["on_add_article_page"] = True
        return context

    def form_valid(
        self, form: AddArticleForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        heading = form.cleaned_data.get("heading")
        full_text = form.cleaned_data.get("full_text")

        Article.objects.create(
            heading=heading, full_text=full_text, author=self.request.user
        )

        return redirect("home")
