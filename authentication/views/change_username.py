
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms import ChangeUsernameForm
from authentication.models import User
from main.utils import DataMixin


class ChangeUsername(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_username.html"
    form_class = ChangeUsernameForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change username")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangeUsernameForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        new_username = form.cleaned_data.get("new_username")
        user_exists = User.objects.filter(username=new_username).exists()

        if user_exists:
            form.add_error("new_username", "This username already exist")
            return self.form_invalid(form)

        self.request.user.username = new_username
        self.request.user.save()

        return redirect("profile", username=new_username)
