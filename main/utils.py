from typing import Any
from django.core.paginator import Paginator
from django.http import HttpRequest

from authentication.models import Profile


class DataMixin():
    login_url = "log_in"

    def get_base_context(self, name: str, **kwargs) -> dict[str, Any]:
        """Returns a base context dict with passed name and kwargs"""

        return get_base_context(self.request, name, **kwargs)


def get_base_context(
    request: HttpRequest, name: str, **kwargs
) -> dict[str, Any]:
    """Returns a base context dict with passed name and kwargs"""
    context = kwargs
    context["name"] = name
    context["user_profile"] = Profile.objects.get(
        user=request.user
    ) if request.user.is_authenticated else None

    return context


def get_paginator_context(
    request: HttpRequest, object_list: Any, name: str, **kwargs
) -> dict[str, Any]:
    """get_base_context with paginator"""
    # Pagination
    paginator = Paginator(object_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Context
    context = get_base_context(request, name, **kwargs)
    context["page_obj"] = page_obj

    return context
