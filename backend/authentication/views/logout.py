from django.contrib.auth import logout as django_logout
from django.http import HttpRequest, HttpResponseRedirect


def logout(request: HttpRequest) -> HttpResponseRedirect:
    django_logout(request)
    return HttpResponseRedirect("/")
