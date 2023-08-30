from datetime import datetime
from random import randint

from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import F, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView

from django_markup.markup import formatter
from .models import *
from .forms import *
from .utils import *


# Home
class Home(DataMixin, ListView):
    model = Article
    template_name = "main/home.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Home")

        return dict(list(context.items()) + list(base.items()))


# Sign up
class SignUp(DataMixin, CreateView):
    form_class = SignUpForm
    template_name = "main/auth/sign_up.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Sign up")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
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
                form.add_error("email", 
                            "This email already busy")
            except User.DoesNotExist:
                pass

        if form.errors:
            return self.form_invalid(form)

        # Creating a new user
        user = User.objects.create_user(username, email, password)
        pfp = request.FILES.get("pfp")

        if pfp is not None:
            # Creating a new profile with pfp
            Profile.objects.create(
                user=user,
                pfp=pfp
            )
        else:
            # Creating a new profile without pfp
            Profile.objects.create(user=user)

        # Authentication
        authenticated_user = authenticate(
            request,
            username=username,
            password=password,
            email=email
        )

        login(request, authenticated_user)

        return redirect("home")


# Log in
class Login(DataMixin, FormView):
    template_name = "main/auth/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Log in")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        # Getting data from a form
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # Authentication
        user = authenticate(
            self.request,
            username=username,
            password=password,
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


# Change username
class ChangeUsername(DataMixin, LoginRequiredMixin, FormView):
    template_name = "main/auth/change_username.html"
    form_class = ChangeUsernameForm
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change username")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        # Getting username from a form and uniqueness check
        new_username = form.cleaned_data.get("new_username")
        user_exists = User.objects.filter(
                                username=new_username).exists()

        if user_exists:
            form.add_error("new_username", "This username already exist")
            return self.form_invalid(form)

        # Changing username and saving changes
        user = User.objects.get(
                            username=self.request.user.username)
        user.username = new_username
        user.save()

        return redirect("see_profile", username=new_username)


# Change password
class ChangePassword(DataMixin, LoginRequiredMixin, FormView):
    template_name = "main/auth/change_password.html"
    form_class = ChangePasswordForm
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change password")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
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


# Change pfp
class ChangePfp(DataMixin, LoginRequiredMixin, FormView):
    template_name = "main/auth/change_pfp.html"
    form_class = ChangePfpForm
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Change profile picture")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
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


# Log out
def logout_user(request):
    logout(request)

    return HttpResponseRedirect("/")


# Adding article
class AddArticle(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = "main/articles/add_article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # on_article_page for illumination of add article button
        base = self.get_base_context("Add article",     
                                            on_add_article_page=1)

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        request = self.request

        # Getting data from a form and format text to markdown
        headling = form.cleaned_data.get("headling")
        full_text = form.cleaned_data.get("full_text")
        full_text = formatter(full_text, "markdown")

        # Creating a new article
        profile = Profile.objects.get(user=request.user)
        Article.objects.create(
            headling=headling, full_text=full_text, author=profile)

        return redirect("home")


# Reading article page
class ReadArticle(DataMixin, DetailView):
    model = Article
    template_name = "main/articles/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Getting article by passed id
        article = context["article"]
        # +1 viewing
        article.viewings = F("viewings") + 1
        article.save()
        base = self.get_base_context(article.headling, 
                                                article=article)

        return dict(list(context.items()) + list(base.items()))


# Delete article
def delete_article(request, pk):
    # Getting article
    article = Article.objects.get(pk=pk)

    # If user is author or staff
    if request.user == article.author.user or request.user.is_staff:
        article.delete()

    return redirect("home")


# Update article
class UpdateArticle(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "main/articles/update_article.html"
    form_class = AddArticleForm
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Update article")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(self, form):
        # Getting article by passed id
        article = get_object_or_404(Article, pk=self.kwargs["pk"])

        # Updating data
        article.update = datetime.now()
        article.headling = form.cleaned_data.get("headling")
        article.full_text = form.cleaned_data.get("full_text")
        article.save()

        return redirect("read", pk=self.kwargs["pk"])


# Random article
def random_article(request):
    # Getting total number of articles
    total_number = Article.objects.count()

    pk = 0
    while True:
        # Generating random id
        pk = randint(1, total_number)
        
        # If article with this id exist
        try:
            Article.objects.get(pk=pk)
            break
        except Article.DoesNotExist:
            continue

    # Redirect to random article
    return redirect("read", pk=pk)


# Comments
def see_comments(request, pk):
    # Getting comments by related article
    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(
                            article=article
                        ).values("profile", "profile__pfp", "pk",
                        "article__pk", "profile__user__username", 
                        "update", "pub_date", "text")
    
    context = get_paginator_context(request, comments, 
                f"Comments to article \"{article.headling}\".",
                article=article)

    return render(request, "main/comments/comments.html", context)


# Add comment
class AddComment(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddCommentForm
    template_name = "main/comments/add_comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Add comment")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        # Getting article pk, data from from and etc.
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(user=self.request.user)
        article = Article.objects.get(pk=pk)
        text = form.cleaned_data.get("text")

        # Creating a new comment
        Comment.objects.create(profile=profile, article=article, text=text)

        return redirect("comments", pk=pk)


# Delete comment
def delete_comment(request, pk, comment_pk):
    # Getting article and related comment
    comment = Comment.objects.get(pk=comment_pk)
    article = Article.objects.get(pk=pk)

    # Author and related article check
    if request.user != comment.profile.user:
        return redirect("home")
    if comment.article != article:
        return redirect("home")
    
    # If all valid
    comment.delete()
    
    return redirect("comments", pk=pk)


# Update comment
class UpdateComment(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "main/comments/update_comment.html"
    form_class = AddCommentForm
    model = Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Update comment")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        # Getting comment
        comment = get_object_or_404(Comment, 
                            pk=self.kwargs['pk'], 
                            article_id=self.kwargs["article_pk"])

        # Updating
        comment.update = datetime.now()
        comment.text = form.cleaned_data.get("text")
        comment.save()

        # Redirect to commented article
        return redirect("comments", pk=self.kwargs["article_pk"])


# Popular and latest articles
def see_all(request, order_by):
    # GET query check
    if order_by == "latest":
        field = "-pub_date"
        name = "Latest articles"
    elif order_by == "popular":
        field = "-viewings"
        name = "Popular articles \U0001F525"
    else:
        raise Http404()

    # Getting articles
    articles = Article.objects.order_by(field).values("headling",
                "full_text", "update", "pub_date", "pk", 
                "author", "author__pfp", "author__user__username")

    context = get_paginator_context(request, articles, name)

    return render(request, "main/articles/see_all.html", context)


# About site
def about(request):
    context = get_base_context(request, "About site")

    return render(request, "main/about.html", context)


# Search
class Search(DataMixin, FormView):
    template_name = "main/search/search.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # on_search_page for illumination of search button
        base = self.get_base_context("Search", on_search_page=1)

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        search_query = form.cleaned_data.get("search_query")

        return redirect("search_results", query=search_query)


# Search results
def search_results(request, query):
    # Searching articles
    articles = Article.objects.filter(
                # By headling
                Q(headling__iregex=query) | 
                # Full text
                Q(full_text__iregex=query) |
                # Author username
                Q(author__user__username__iregex=query)
                ).values(
                    "headling", "full_text", "update", 
                    "pub_date", "pk", "author", "author__pfp", 
                    "author__user__username"
                )

    context = get_paginator_context(request, articles, 
                    f"Search results by query: \"{query}\"", 
                    on_search_page=1
                )

    return render(request, "main/search/search_results.html", context)


# Profile page
def see_profile(request, username: str):
    # Getting user articles
    articles = Article.objects.filter(
                            author__user__username=username
                    ).values(
                        "headling", "full_text", "update", 
                        "pub_date", "pk", "author", "author__pfp", 
                        "author__user__username"
                        )
    
    context = get_paginator_context(request, articles, 
                            f"{username.title()}'s profile",
                            profile=get_object_or_404(
                                Profile, user__username=username)
                            )

    return render(request, "main/profile/profile.html", context)


# Profile settings
def profile_settings(request, username):
    # Getting profile or raising 404
    user = request.user
    profile = get_object_or_404(Profile, user__username=username)

    # Validation
    valid = 0
    if user.is_authenticated and user.username == username:
        valid = 1

    context = get_base_context(
                        request, f"{username.title()}'s profile settings",
                        profile=profile, valid=valid
                    )

    return render(request, "main/profile/settings.html", context)


# Feedback
class Feedback(DataMixin, FormView):
    template_name = "main/feedbacks/feedback.html"
    form_class = FeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Feedback")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        if form.is_valid():
            # Getting data from a form
            headling = "Blogioma report: " + form.cleaned_data.get("problem")
            desc = form.cleaned_data.get("problem_desc")
            email = form.cleaned_data.get("email")

            # Attachment user email to the mail
            desc += f"\n\n\nUser email: {email}"

            # Sending mail
            sended_email = EmailMessage(
                                headling, desc, 
                                settings.EMAIL_HOST_USER,
                                [settings.EMAIL_HOST_USER]
                            )
            sended_email.send(fail_silently=False)

            return render(
                    self.request, 
                    "main/feedbacks/feedback_success.html", 
                    self.get_context_data()
                )
        
        return self.form_invalid(form)


# Report on article
class ReportArticle(DataMixin, LoginRequiredMixin, CreateView):
    template_name = "main/feedbacks/report.html"
    form_class = ReportForm
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Report on article")

        return dict(list(context.items()) + list(base.items()))
    
    def form_valid(self, form):
        # Getting data from a form
        reason = form.cleaned_data.get("reason")
        desc = form.cleaned_data.get("desc")

        # Getting an reported article
        article_pk = self.kwargs.get("pk")
        article = Article.objects.get(pk=article_pk)

        # Creating report
        Report.objects.create(reason=reason, desc=desc, article=article)
        article.reports = F("reports") + 1

        return redirect("home")
