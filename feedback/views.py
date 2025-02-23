from typing import Any
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView

from articles.models import Article
from main.utils import DataMixin
from .forms import FeedbackForm, ReportForm
from .models import Report
from .tasks import send_feedback


class Feedback(DataMixin, FormView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context(
            "Feedback", email=settings.EMAIL_HOST_USER
        )

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form: FeedbackForm) -> HttpResponse:
        if form.is_valid():
            # Getting data from a form
            heading = "Blogioma report: " + form.cleaned_data.get("problem")
            desc = form.cleaned_data.get("problem_desc")
            email = form.cleaned_data.get("email")

            # Attachment user email to the mail
            desc += f"\n\n\nUser email: {email}"

            # Sending mail
            send_feedback.delay(heading, desc)

            return render(
                self.request, "feedback/feedback_success.html",
                self.get_context_data()
            )

        return self.form_invalid(form)


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
        # Getting data from a form
        reason = form.cleaned_data.get("reason")
        desc = form.cleaned_data.get("desc")

        # Getting a reported article
        article_pk = self.kwargs.get("pk")
        article = Article.objects.get(pk=article_pk)

        # Creating report
        report = Report.objects.create(
            reason=reason,
            desc=desc,
            reported_article=article,
            owner=self.request.user
        )
        article.reports.add(report)

        return redirect("home")
