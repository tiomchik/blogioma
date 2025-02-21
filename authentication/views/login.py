from typing import Any
from django.contrib.auth import authenticate, login
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms.login import LoginForm
from main.utils import DataMixin


class Login(DataMixin, FormView):
    template_name = "auth/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Log in")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: LoginForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(
            self.request, username=username, password=password,
        )

        if user:
            login(self.request, user)
            return redirect("home")

        form.add_error("password", "Invalid username and/or password")

        return self.form_invalid(form)
