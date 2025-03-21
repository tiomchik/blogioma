from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from articles.models import Article
from main.utils import DataMixin
from feedback.forms.report import ReportForm
from feedback.models import Report


class ReportArticle(DataMixin, LoginRequiredMixin, CreateView):
    template_name = "feedback/report.html"
    form_class = ReportForm
    model = Report

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Report on article")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ReportForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        reason = form.cleaned_data.get("reason")
        desc = form.cleaned_data.get("desc")
        article = self.get_reported_article()

        report = Report.objects.create(
            reason=reason,
            desc=desc,
            reported_article=article,
            owner=self.request.user
        )
        article.reports.add(report)

        return redirect("home")

    def get_reported_article(self) -> Article:
        article_pk = self.kwargs.get("pk")
        return Article.objects.get(pk=article_pk)
