from typing import Any
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from search.forms import SearchForm
from main.mixins import DataMixin


class Search(DataMixin, FormView):
    template_name = "search/search.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Search"
        context["illuminate_search_button"] = True
        return context

    def form_valid(
        self, form: SearchForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        search_query = form.cleaned_data.get("search_query")

        return redirect("search_results", query=search_query)
