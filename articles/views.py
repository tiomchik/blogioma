from typing import Any
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect,
    HttpResponseRedirect, HttpRequest
)

from articles.utils import get_random_article
from main.utils import DataMixin, get_paginator_context
from .forms import AddArticleForm
from .models import Article


class AddArticle(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = "articles/add_article.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # on_add_article_page for illumination of add article button
        base = self.get_base_context("Add article", on_add_article_page=1)

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: AddArticleForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        heading = form.cleaned_data.get("heading")
        full_text = form.cleaned_data.get("full_text")

        Article.objects.create(
            heading=heading, full_text=full_text, author=self.request.user
        )

        return redirect("home")


class ReadArticle(DataMixin, DetailView):
    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        article: Article = context["article"]
        article.increment_viewings()
        article.save_and_refresh()
        base = self.get_base_context(article.heading, article=article)
        return dict(list(context.items()) + list(base.items()))


def delete_article(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    article = Article.objects.get(pk=pk)

    if request.user == article.author or request.user.is_staff:
        article.delete()

    return redirect("home")


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

        article.update = timezone.now()
        article.heading = form.cleaned_data.get("heading")
        article.full_text = form.cleaned_data.get("full_text")
        article.save()

        return redirect("read", pk=self.kwargs["pk"])


def random_article(
    request: HttpRequest
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    article = get_random_article()
    return redirect("read", pk=article.pk)


@cache_page(30)
def see_all(request: HttpRequest, order_by: str) -> HttpResponse:
    if order_by == "latest":
        field = "-pub_date"
        name = "Latest articles"
    elif order_by == "popular":
        field = "-viewings"
        name = "Popular articles \U0001F525"
    else:
        raise Http404()

    articles = Article.objects.order_by(field).values(
        "heading", "full_text", "update", "pub_date", "pk", 
        "author", "author__pfp", "author__username"
    )

    context = get_paginator_context(request, articles, name)

    return render(request, "articles/see_all.html", context)
