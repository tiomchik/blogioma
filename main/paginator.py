from django.core.paginator import Paginator, Page
from django.http import HttpRequest


def get_page_obj(request: HttpRequest, object_list: list) -> Page:
    paginator = Paginator(object_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj
