from typing import Any
from django.contrib.auth import login
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from authentication.forms.sign_up import SignUpForm
from authentication.models import User
from main.utils import DataMixin


class SignUp(DataMixin, CreateView):
    form_class = SignUpForm
    template_name = "auth/sign_up.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Sign up")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: SignUpForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.validate_passwords_match(form)
        self.validate_email_uniqness(form)

        self.show_form_errors_if_exist(form)

        user = self.create_user(form)
        login(self.request, user)
        return redirect("home")

    def validate_passwords_match(self, form: SignUpForm) -> None:
        password = form.cleaned_data.get("password")
        password1 = form.cleaned_data.get("password1")
        if password != password1:
            form.add_error("password1", "Password's don't match")

    def validate_email_uniqness(self, form: SignUpForm) -> None:
        email = form.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            form.add_error("email", "This email already busy")

    def create_user(self, form: SignUpForm) -> User:
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email") or None
        password = form.cleaned_data.get("password")
        pfp = self.request.FILES.get("pfp")
        return User.objects.create(
            username=username, email=email, password=password, pfp=pfp
        )
