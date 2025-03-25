from typing import Any
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.forms.change_pfp import ChangePfpForm
from authentication.models import User
from main.mixins import DataMixin


class ChangePfp(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_pfp.html"
    form_class = ChangePfpForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Change profile picture"
        return context

    def form_valid(
        self, form: ChangePfpForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        new_pfp = form.cleaned_data.get("new_pfp")
        self.request.user.pfp = new_pfp
        self.request.user.save()
        return redirect("profile", username=self.request.user.username)
