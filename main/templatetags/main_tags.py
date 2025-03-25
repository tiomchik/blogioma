from django import template
from django.core.paginator import Page

from articles.utils import get_articles_ordered_by_field

register = template.Library()


@register.inclusion_tag("main/tags/for_articles.html")
def show_page_obj_articles(page_obj: Page):
    return {"articles_for": page_obj}


@register.inclusion_tag("main/tags/for_articles.html")
def show_6_articles(order_by: str):
    return {"articles_for": get_articles_ordered_by_field(order_by)[:6]}


@register.inclusion_tag("main/tags/form.html")
def show_form(form):
    return {"form": form}


@register.inclusion_tag("main/tags/paginator.html")
def paginator(page_obj):
    return {"page_obj": page_obj}
