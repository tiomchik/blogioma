
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.edit import UpdateView

from authentication.forms.social_media_links import SocialMediaLinksForm
from authentication.models import User
from main.mixins import DataMixin


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
