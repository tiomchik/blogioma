from django.utils import timezone
from typing import Any
from django.http import (
    HttpRequest, HttpResponse, HttpResponsePermanentRedirect,
    HttpResponseRedirect
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, UpdateView

from articles.models import Article
from main.utils import get_paginator_context, DataMixin
from .forms import AddCommentForm
from .models import Comment


@cache_page(30)
def see_comments(request: HttpRequest, pk: int) -> HttpResponse:
    # Getting comments by related article
    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article).values(
        "profile", "profile__pfp", "pk", "article__pk",
        "profile__username", "update", "pub_date", "text"
    )

    context = get_paginator_context(
        request, object_list=comments,
        name=f"Comments to article \"{article.heading}\".",
        article=article
    )

    return render(request, "comments/comments.html", context)


class AddComment(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddCommentForm
    template_name = "comments/add_comment.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Add comment")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: AddCommentForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        # Getting article pk, data from from and etc.
        pk = self.kwargs["pk"]
        article = Article.objects.get(pk=pk)
        text = form.cleaned_data.get("text")

        # Creating a new comment
        Comment.objects.create(
            profile=self.request.user, article=article, text=text
        )

        return redirect("comments", pk=pk)


def delete_comment(
    request: HttpRequest, pk: int, comment_pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    # Getting article and related comment
    comment = Comment.objects.get(pk=comment_pk)
    article = Article.objects.get(pk=pk)

    # Author and related article check
    if request.user != comment.profile:
        return redirect("home")
    if comment.article != article:
        return redirect("home")

    # If all valid
    comment.delete()

    return redirect("comments", pk=pk)


class UpdateComment(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = "comments/update_comment.html"
    form_class = AddCommentForm
    model = Comment

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base = self.get_base_context("Update comment")

        return dict(list(context.items()) + list(base.items()))

    def form_valid(
        self, form: AddCommentForm
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        # Getting comment
        comment = get_object_or_404(
            Comment, pk=self.kwargs["pk"],
            article_id=self.kwargs["article_pk"]
        )

        # Updating
        comment.update = timezone.now()
        comment.text = form.cleaned_data.get("text")
        comment.save()

        # Redirect to commented article
        return redirect("comments", pk=self.kwargs["article_pk"])
