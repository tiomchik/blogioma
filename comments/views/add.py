from typing import Any
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from articles.utils import get_article_by_pk
from main.mixins import DataMixin
from comments.forms import AddCommentForm
from comments.models import Comment


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
