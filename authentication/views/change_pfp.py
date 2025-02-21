from typing import Any
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.forms.change_pfp import ChangePfpForm
from authentication.models import User
from main.utils import DataMixin


class ChangePfp(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_pfp.html"
    form_class = ChangePfpForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change profile picture")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangePfpForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        new_pfp = form.cleaned_data.get("new_pfp")
        if not new_pfp:
            form.add_error("new_pfp", "This field is required")
            return self.form_invalid(form)

        self.request.user.pfp = new_pfp
        self.request.user.save()

        return redirect("profile", username=self.request.user.username)
