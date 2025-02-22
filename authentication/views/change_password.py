from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms.change_password import ChangePasswordForm
from authentication.models import User
from main.utils import DataMixin


class ChangePassword(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_password.html"
    form_class = ChangePasswordForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change password")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangePasswordForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.validate_passwords_match(form)
        if form.errors:
            return self.form_invalid(form)
        self.set_new_password(form)
        return redirect(self.login_url)

    def validate_passwords_match(self, form: ChangePasswordForm) -> None:
        new_password = form.cleaned_data.get("new_password")
        new_password1 = form.cleaned_data.get("new_password1")
        if new_password != new_password1:
            form.add_error("new_password1", "Password's don't match")

    def set_new_password(self, form: ChangePasswordForm) -> None:
        new_password = form.cleaned_data.get("new_password")
        self.request.user.set_password(new_password)
        self.request.user.save()
