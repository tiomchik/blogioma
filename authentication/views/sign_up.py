from typing import Any
from django.contrib.auth import login
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from authentication.forms.sign_up import SignUpForm
from authentication.models import User
from main.mixins import DataMixin


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
        if not self.is_passwords_match(form):
            form.add_error("password1", "Password's don't match")
            return self.form_invalid(form)
        if self.is_email_not_blank(form) and not self.is_email_unique(form):
            form.add_error("email", "This email already busy")
            return self.form_invalid(form)

        user = self.create_user(form)
        login(self.request, user)
        return redirect("home")

    def is_passwords_match(self, form: SignUpForm) -> bool:
        password = form.cleaned_data.get("password")
        password1 = form.cleaned_data.get("password1")
        return password == password1

    def is_email_not_blank(self, form: SignUpForm) -> bool:
        email = form.cleaned_data.get("email")
        return bool(email)

    def is_email_unique(self, form: SignUpForm) -> bool:
        email = form.cleaned_data.get("email")
        return not User.objects.filter(email=email).exists()

    def create_user(self, form: SignUpForm) -> User:
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email") or None
        password = form.cleaned_data.get("password")
        pfp = self.request.FILES.get("pfp")
        return User.objects.create(
            username=username, email=email, password=password, pfp=pfp
        )
