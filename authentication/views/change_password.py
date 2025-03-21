from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms.change_password import ChangePasswordForm
from authentication.models import User
from main.mixins import DataMixin


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
        if not self.is_passwords_match(form):
            form.add_error("new_password1", "Password's don't match")
            return self.form_invalid(form)

        self.set_new_password(form)
        return redirect(self.login_url)

    def is_passwords_match(self, form: ChangePasswordForm) -> bool:
        new_password = form.cleaned_data.get("new_password")
        new_password1 = form.cleaned_data.get("new_password1")
        return new_password == new_password1

    def set_new_password(self, form: ChangePasswordForm) -> None:
        new_password = form.cleaned_data.get("new_password")
        self.request.user.set_password(new_password)
        self.request.user.save()
