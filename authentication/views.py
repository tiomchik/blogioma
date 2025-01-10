from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import (
    HttpRequest, HttpResponse, HttpResponsePermanentRedirect,
    HttpResponseRedirect
)
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, FormView, UpdateView

from main.utils import DataMixin, get_paginator_context, get_base_context
from articles.models import Article
from .forms import (
    SignUpForm, LoginForm, ChangeUsernameForm, ChangePasswordForm,
    ChangePfpForm, SocialMediaLinksForm
)
from .models import User


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

        pfp = request.FILES.get("pfp")
        user = User.objects.create(
            username=username, email=email, password=password, pfp=pfp
        )

        login(request, user)

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

        return redirect("see_profile", username=new_username)


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
        new_password = form.cleaned_data.get("new_password")
        new_password1 = form.cleaned_data.get("new_password1")

        if new_password != new_password1:
            form.add_error("new_password1", "Password's don't match")
            return self.form_invalid(form)

        self.request.user.set_password(new_password)
        self.request.user.save()

        return redirect(self.login_url)


class ChangePfp(DataMixin, LoginRequiredMixin, FormView):
    template_name = "auth/change_pfp.html"
    form_class = ChangePfpForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change profile picture")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: ChangePfpForm
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        new_pfp = form.cleaned_data.get("new_pfp")
        if not new_pfp:
            form.add_error("new_pfp", "This field is required")
            return self.form_invalid(form)

        self.request.user.pfp = new_pfp
        self.request.user.save()

        return redirect("see_profile", username=self.request.user.username)


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return HttpResponseRedirect("/")


@cache_page(30)
def see_profile(request: HttpRequest, username: str) -> HttpResponse:
    articles = Article.objects.filter(author__username=username).values(
        "heading", "full_text", "update", 
        "pub_date", "pk", "author", "author__pfp", 
        "author__username"
    )

    context = get_paginator_context(
        request, articles, f"{username}'s profile",
        profile=get_object_or_404(User, username=username)
    )

    return render(request, "profile/profile.html", context)


@cache_page(60 * 30)
def profile_settings(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)

    valid = 0
    if request.user.is_authenticated and request.user.username == username:
        valid = 1

    context = get_base_context(
        request, name=f"{username}'s profile settings",
        profile=user, valid=valid
    )

    return render(request, "profile/settings.html", context)


class SocialMediaLinks(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "profile/social_media_links.html"
    form_class = SocialMediaLinksForm
    model = User

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Social media links")

        return dict(list(context.items()) + list(base.items()))

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> User:
        return self.request.user
