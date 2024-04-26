from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse, HttpResponsePermanentRedirect,
    HttpResponseRedirect
)
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, FormView

from main.utils import DataMixin, get_paginator_context, get_base_context
from articles.models import Article
from .forms import (
    SignUpForm, LoginForm, ChangeUsernameForm, ChangePasswordForm,
    ChangePfpForm
)
from .models import Profile


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

        # Getting data from a form
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        password1 = form.cleaned_data.get("password1")

        if password != password1:
            form.add_error("password1", "Password's don't match")

        # Email and username uniqueness check
        try:
            User.objects.get(username=username)
            form.add_error("username", "This username already exist")
        except User.DoesNotExist:
            pass

        if "@" in email:
            try:
                User.objects.get(email=email)
                form.add_error("email", "This email already busy")
            except User.DoesNotExist:
                pass

        if form.errors:
            return self.form_invalid(form)

        # Creating a new user
        user = User.objects.create_user(username, email, password)
        pfp = request.FILES.get("pfp")

        if pfp is not None:
            # Creating a new profile with pfp
            Profile.objects.create(user=user, pfp=pfp)
        else:
            # Creating a new profile without pfp
            Profile.objects.create(user=user)

        # Authentication
        authenticated_user = authenticate(
            request, username=username, password=password, email=email
        )

        login(request, authenticated_user)

        return redirect("home")


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
        # Getting data from a form
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # Authentication
        user = authenticate(
            self.request, username=username, password=password,
        )

        # If valid
        if user:
            login(self.request, user)
            return redirect("home")

        # If invalid
        form.add_error("password", 
            "Invalid username and/or password")
        # Showing form with errors
        return self.form_invalid(form)


class ChangeUsername(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_username.html"
    form_class = ChangeUsernameForm
    model = Profile

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change username")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangeUsernameForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        # Getting username from a form and uniqueness check
        new_username = form.cleaned_data.get("new_username")
        user_exists = User.objects.filter(username=new_username).exists()

        if user_exists:
            form.add_error("new_username", "This username already exist")
            return self.form_invalid(form)

        # Changing username and saving changes
        user = User.objects.get(username=self.request.user.username)
        user.username = new_username
        user.save()

        return redirect("see_profile", username=new_username)


class ChangePassword(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_password.html"
    form_class = ChangePasswordForm
    model = Profile

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change password")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangePasswordForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        # Getting data from a form
        new_password = form.cleaned_data.get("new_password")
        new_password1 = form.cleaned_data.get("new_password1")

        # If the passwords dont match
        if new_password != new_password1:
            form.add_error("new_password1", "Password's don't match")
            return self.form_invalid(form)

        # Else
        user = self.request.user
        user.set_password(new_password)
        user.save()

        return redirect(self.login_url)


class ChangePfp(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_pfp.html"
    form_class = ChangePfpForm
    model = Profile

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change profile picture")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangePfpForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        # Getting a new pfp from a form
        new_pfp = form.cleaned_data.get("new_pfp")
        if not new_pfp:
            form.add_error("new_pfp", "This field is required")
            return self.form_invalid(form)

        # Getting user and changing pfp
        user = Profile.objects.get(user=self.request.user)
        user.pfp = new_pfp
        user.save()

        return redirect("see_profile", username=user.user.username)


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return HttpResponseRedirect("/")


def see_profile(request: HttpRequest, username: str) -> HttpResponse:
    # Getting user articles
    articles = Article.objects.filter(author__user__username=username).values(
        "headling", "full_text", "update", 
        "pub_date", "pk", "author", "author__pfp", 
        "author__user__username"
    )

    context = get_paginator_context(
        request, articles, f"{username}'s profile",
        profile=get_object_or_404(Profile, user__username=username)
    )

    return render(request, "profile/profile.html", context)


def profile_settings(request: HttpRequest, username: str) -> HttpResponse:
    # Getting profile or raising 404
    user = request.user
    profile = get_object_or_404(Profile, user__username=username)

    # Validation
    valid = 0
    if user.is_authenticated and user.username == username:
        valid = 1

    context = get_base_context(
        request, name=f"{username}'s profile settings",
        profile=profile, valid=valid
    )

    return render(request, "profile/settings.html", context)
