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

from articles.utils import get_article_by_pk
from main.utils import get_paginator_context, DataMixin
from .forms import AddCommentForm
from .models import Comment


@cache_page(30)
def see_comments(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_article_by_pk(pk)
    comments = Comment.objects.filter(article=article).values(
        "author", "author__pfp", "pk", "article__pk",
        "author__username", "update", "pub_date", "text"
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
        pk = self.kwargs["pk"]
        article = get_article_by_pk(pk)
        text = form.cleaned_data.get("text")

        Comment.objects.create(
            author=self.request.user, article=article, text=text
        )

        return redirect("comments", pk=pk)


def delete_comment(
    request: HttpRequest, pk: int, comment_pk: int
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    comment = Comment.objects.get(pk=comment_pk)
    article = get_article_by_pk(pk)

    if request.user != comment.author:
        return redirect("home")
    if comment.article != article:
        return redirect("home")

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
        comment = get_object_or_404(
            Comment, pk=self.kwargs["pk"],
            article_id=self.kwargs["article_pk"]
        )

        comment.update = timezone.now()
        comment.text = form.cleaned_data.get("text")
        comment.save()

        return redirect("comments", pk=self.kwargs["article_pk"])
