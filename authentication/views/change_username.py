
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms.change_username import ChangeUsernameForm
from authentication.models import User
from main.mixins import DataMixin


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
        if not self.is_username_unique(form):
            form.add_error("new_username", "This username already busy")
            return self.form_invalid(form)

        self.set_new_username(form)
        return redirect("profile", username=self.request.user.username)

    def is_username_unique(self, form: ChangeUsernameForm) -> bool:
        new_username = form.cleaned_data.get("new_username")
        return not User.objects.filter(username=new_username).exists()

    def set_new_username(self, form: ChangeUsernameForm) -> None:
        new_username = form.cleaned_data.get("new_username")
        self.request.user.username = new_username
        self.request.user.save()
