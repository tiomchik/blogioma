from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView

from main.utils import DataMixin
from articles.models import Article
from .forms import FeedbackForm, ReportForm
from .models import Report


class Feedback(DataMixin, FormView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Feedback")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        if form.is_valid():
            # Getting data from a form
            headling = "Blogioma report: " + form.cleaned_data.get("problem")
            desc = form.cleaned_data.get("problem_desc")
            email = form.cleaned_data.get("email")

            # Attachment user email to the mail
            desc += f"\n\n\nUser email: {email}"

            # Sending mail
            sended_email = EmailMessage(
                                headling, desc, 
                                settings.EMAIL_HOST_USER,
                                [settings.EMAIL_HOST_USER]
                            )
            sended_email.send(fail_silently=False)

            return render(
                    self.request, 
                    "main/feedbacks/feedback_success.html", 
                    self.get_context_data()
                )
        
        return self.form_invalid(form)


class ReportArticle(DataMixin, LoginRequiredMixin, CreateView):
    template_name = "feedback/report.html"
    form_class = ReportForm
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Report on article")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        # Getting data from a form
        reason = form.cleaned_data.get("reason")
        desc = form.cleaned_data.get("desc")

        # Getting an reported article
        article_pk = self.kwargs.get("pk")
        article = Article.objects.get(pk=article_pk)

        # Creating report
        Report.objects.create(reason=reason, desc=desc, article=article)
        article.reports = F("reports") + 1

        return redirect("home")
