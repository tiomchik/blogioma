from django import template

from articles.utils import get_articles_ordered_by_field

register = template.Library()


# Showing articles
@register.inclusion_tag("main/tags/for_articles.html")
def show_articles(order_by: str = "-pub_date", only_6=None, page_obj=None):
    context = {}
    if page_obj:
        context["articles_for"] = page_obj
    else:
        if only_6:
            context["articles_for"] = get_articles_ordered_by_field(
                order_by
            )[:6]
        else:
            context["articles_for"] = get_articles_ordered_by_field(order_by)

    return context


# Showing form
@register.inclusion_tag("main/tags/form.html")
def show_form(form):
    return {"form": form}


# Showing paginator
@register.inclusion_tag("main/tags/paginator.html")
def paginator(page_obj):
    return {"page_obj": page_obj}
