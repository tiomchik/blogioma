from django.utils import timezone
from typing import Any
from django.http import (
    HttpResponsePermanentRedirect, HttpResponseRedirect
)
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from main.utils import DataMixin
from comments.forms import AddCommentForm
from comments.models import Comment


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
        self.update_and_save(comment, form)
        return redirect("comments", pk=self.kwargs["article_pk"])

    def update_and_save(self, comment: Comment, form: AddCommentForm) -> None:
        comment.update = timezone.now()
        comment.text = form.cleaned_data.get("text")
        comment.save()
