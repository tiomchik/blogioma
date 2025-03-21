from typing import Any
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from search.forms import SearchForm
from main.utils import DataMixin


class Search(DataMixin, FormView):
    template_name = "search/search.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # on_search_page for illumination of search button
        base = self.get_base_context("Search", on_search_page=1)

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: SearchForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        search_query = form.cleaned_data.get("search_query")

        return redirect("search_results", query=search_query)
