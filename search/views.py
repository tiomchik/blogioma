from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic.edit import FormView

from .forms import SearchForm
from articles.models import Article
from main.utils import get_paginator_context, DataMixin


class Search(DataMixin, FormView):
    template_name = "search/search.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # on_search_page for illumination of search button
        base = self.get_base_context("Search", on_search_page=1)

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        search_query = form.cleaned_data.get("search_query")

        return redirect("search_results", query=search_query)


def search_results(request, query):
    # Searching articles
    articles = Article.objects.filter(
        # By headling
        Q(headling__iregex=query) | 
        # Full text
        Q(full_text__iregex=query) |
        # Author username
        Q(author__user__username__iregex=query)
    ).values(
        "headling", "full_text", "update", "pub_date", "pk",
        "author", "author__pfp", "author__user__username"
    )

    context = get_paginator_context(
        request, articles, f"Search results by query: \"{query}\"",
        on_search_page=1
    )

    return render(request, "search/search_results.html", context)
