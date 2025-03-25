from typing import Any
from django.core.paginator import Paginator
from django.http import HttpRequest


def get_base_context(name: str, **kwargs) -> dict[str, Any]:
    context = kwargs
    context["name"] = name
    return context


def get_paginator_context(
    request: HttpRequest, object_list: Any, name: str, **kwargs
) -> dict[str, Any]:
    paginator = Paginator(object_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = get_base_context(name, **kwargs)
    context["page_obj"] = page_obj

    return context
