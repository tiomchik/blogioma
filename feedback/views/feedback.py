from typing import Any
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView

from main.utils import DataMixin
from feedback.forms.feedback import FeedbackForm
from feedback.tasks import send_feedback


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
            self.send_feedback(form)
            return render(
                self.request, "feedback/feedback_success.html",
                self.get_context_data()
            )

        return self.form_invalid(form)

    def send_feedback(self, form: FeedbackForm) -> None:
        heading = "Blogioma report: " + form.cleaned_data.get("problem")
        desc = form.cleaned_data.get("problem_desc")
        email = form.cleaned_data.get("email")
        desc += f"\n\n\nUser email: {email}"

        send_feedback.delay(heading, desc)
