from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.http import Http404
from django_markup.markup import formatter
from random import randint

from authentication.models import Profile
from main.utils import DataMixin, get_paginator_context
from .forms import AddArticleForm
from .models import Article


class AddArticle(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = "articles/add_article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # on_article_page for illumination of add article button
        base = self.get_base_context("Add article", on_add_article_page=1)

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        request = self.request

        # Getting data from a form and format text to markdown
        headling = form.cleaned_data.get("headling")
        full_text = form.cleaned_data.get("full_text")
        full_text = formatter(full_text, "markdown")

        # Creating a new article
        profile = Profile.objects.get(user=request.user)
        Article.objects.create(
            headling=headling, full_text=full_text, author=profile
        )

        return redirect("home")


class ReadArticle(DataMixin, DetailView):
    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Getting article by passed id
        article = context["article"]
        # +1 viewing
        article.viewings = F("viewings") + 1
        article.save()
        base = self.get_base_context(article.headling, article=article)

        return dict(list(context.items()) + list(base.items()))


def delete_article(request, pk):
    # Getting article
    article = Article.objects.get(pk=pk)

    # If user is author or staff
    if request.user == article.author.user or request.user.is_staff:
        article.delete()

    return redirect("home")


class UpdateArticle(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "articles/update_article.html"
    form_class = AddArticleForm
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Update article")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        # Getting article by passed id
        article = get_object_or_404(Article, pk=self.kwargs["pk"])

        # Updating data
        article.update = datetime.now()
        article.headling = form.cleaned_data.get("headling")
        article.full_text = form.cleaned_data.get("full_text")
        article.save()

        return redirect("read", pk=self.kwargs["pk"])


def random_article(request):
    # Getting total number of articles
    total_number = Article.objects.count()

    pk = 0
    while True:
        # Generating random id
        pk = randint(1, total_number)
        
        # If article with this id exist
        try:
            Article.objects.get(pk=pk)
            break
        except Article.DoesNotExist:
            continue

    # Redirect to random article
    return redirect("read", pk=pk)


def see_all(request, order_by):
    # GET query check
    if order_by == "latest":
        field = "-pub_date"
        name = "Latest articles"
    elif order_by == "popular":
        field = "-viewings"
        name = "Popular articles \U0001F525"
    else:
        raise Http404()

    # Getting articles
    articles = Article.objects.order_by(field).values(
        "headling", "full_text", "update", "pub_date", "pk", 
        "author", "author__pfp", "author__user__username"
    )

    context = get_paginator_context(request, articles, name)

    return render(request, "articles/see_all.html", context)
