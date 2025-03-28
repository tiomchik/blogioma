from typing import Any
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from authentication.forms.login import LoginForm
from main.mixins import DataMixin


class Login(DataMixin, FormView):
    template_name = "auth/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Log in"
        return context

    def form_valid(
        self, form: LoginForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        user = self.authenticate_user(form)
        if not user:
            form.add_error("password", "Invalid username and/or password")
            return self.form_invalid(form)

        login(self.request, user)
        return redirect("home")

    def authenticate_user(self, form: LoginForm) -> AbstractUser | None:
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        return authenticate(
            self.request, username=username, password=password,
        )
