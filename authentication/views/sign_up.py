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
        request = self.request

        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        password1 = form.cleaned_data.get("password1")

        if password != password1:
            form.add_error("password1", "Password's don't match")

        if "@" in email:
            try:
                User.objects.get(email=email)
                form.add_error("email", "This email already busy")
            except User.DoesNotExist:
                pass

        if form.errors:
            return self.form_invalid(form)

        pfp = request.FILES.get("pfp")
        user = User.objects.create(
            username=username, email=email, password=password, pfp=pfp
        )

        login(request, user)

        return redirect("home")
