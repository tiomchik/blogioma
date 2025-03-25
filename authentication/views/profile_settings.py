from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from authentication.models import User


@cache_page(60 * 30)
def profile_settings(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    context = {
        "name": f"{username}'s profile settings",
        "profile": user
    }
    return render(request, "profile/settings.html", context)
