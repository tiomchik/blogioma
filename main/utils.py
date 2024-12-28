from typing import Any
from collections.abc import Awaitable, Callable, Sequence
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.urls import reverse
from django.urls.conf import _path
from django.urls.resolvers import RoutePattern, URLPattern, URLResolver
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from articles.models import Article
from comments.models import Comment


class DataMixin():
    login_url = "log_in"

    def get_base_context(self, name: str, **kwargs) -> dict[str, Any]:
        """Returns a base context dict with passed name and kwargs"""

        return get_base_context(self.request, name, **kwargs)


class GenericTestCase(APITestCase):
    def setUp(self) -> None:
        data = {"username": "test_user1", "password": "12341234"}
        self._register_user(**data)

        self.user = User.objects.get(username=data["username"])
        self.token = self._obtain_token(**data)
        self.auth_header = {"Authorization": f"Token {self.token}"}

        self.article = self._create_article()
        self.comment = Comment.objects.create(
            text="nice article", article=self.article, profile=self.user
        )

    def setUpSessionAuth(self) -> None:
        """This is another version of the `setUp()` method, created
        for session authentication. To use it, call this method in
        the `setUp()`."""
        user_data = {"username": "test_user", "password": "12341234"}
        self.user = User.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.article = self._create_article()

    def _obtain_token(self, **user_data) -> str:
        """Obtains token according to passed `user_data`."""
        token_url = reverse("obtain-token")
        token: str = self.client.post(
            token_url, user_data
        ).json().get("token")

        return token

    def _register_user(self, **user_data) -> HttpResponse:
        """Registers a user with `user_data`."""
        url = reverse("register")
        return self.client.post(url, user_data)

    def _set_another_user(self, **another_user_data) -> None:
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)
        self.auth_header = {
            "Authorization": f"Token {another_user_token}"
        }

    def assertUnauthResponse(self, r: HttpResponse) -> None:
        """Checks that response is returned error of unauthorized user."""
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            r.json().get("detail"),
            "Authentication credentials were not provided."
        )

    def assertFieldIsRequired(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get(field), ["This field is required."]
        )

    def assertFieldIsTooLong(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        error: str = r.json().get(field)[0]
        self.assertTrue(error.startswith("Ensure this field has no more"))
        self.assertTrue(error.endswith(" characters."))

    def assertForbiddenResponse(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    def _auth_to_another_user(
        self, username: str = "test_user123", password: str = "12341234"
    ) -> None:
        """Authenticates `self.client` using `self.client.login()`
        and another user data."""
        self.client.logout()
        new_user_data = {"username": username, "password": password}
        User.objects.create(**new_user_data)
        self.client.login(**new_user_data)

    def _create_article(
        self, heading: str = "test_article",
        full_text: str = "lorem ipsum dolor"
    ) -> Article:
        """Creates article and returns it."""
        data = {
            "heading": heading, "full_text": full_text,
            "author": self.user
        }
        return Article.objects.create(**data)


def get_base_context(
    request: HttpRequest, name: str, **kwargs
) -> dict[str, Any]:
    """Returns a base context dict with passed name and kwargs"""
    context = kwargs
    context["name"] = name
    if request.user.is_authenticated:
        context["user_profile"] = request.user

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


class PrefixRoutePattern(RoutePattern):
    """A more optimized custom router."""

    def __init__(
        self, route: str, name: str | None = None, is_endpoint: bool = False
    ) -> None:
        idx = route.find("<")

        # If the whole pattern is a constant string and it can be
        # compared with the entire URL.
        if idx == -1:
            self._prefix = route
            self._is_static = True
        else:
            self._is_static = False
            self._prefix = route[:idx]

        self._is_endpoint = is_endpoint
        super().__init__(route, name, is_endpoint)

    def match(
        self, path: str
    ) -> tuple[str, tuple[Any, ...], dict[str, Any]] | None:
        """Returns tuple of: 
        
        1. Rest of the URL
        2. Unnamed variables
        3. Named variables.
        """
        if self._is_static:
            if self._is_endpoint and path == self._prefix:
                return "", (), {}
            elif not self._is_endpoint and path.startswith(self._prefix):
                return path[len(self._prefix) :], (), {}
        else:
            if path.startswith(self._prefix):
                return super().match(path)

        return None


def make_pattern(
    route: str, name: str | None = None, is_endpoint: bool = False
) -> PrefixRoutePattern | RoutePattern:
    idx = route.find("<")
    if idx == -1 or idx > 2:
        return PrefixRoutePattern(route, name, is_endpoint)
    else:
        return RoutePattern(route, name, is_endpoint)


def my_path(
    route: str,
    view: (
        Callable[..., HttpResponseBase | Awaitable[HttpResponseBase]]
        | tuple[Sequence[URLResolver | URLPattern], str | None, str | None]
    ),
    kwargs: dict[str, Any] | None = None,
    name: str | None = None,
) -> URLResolver | URLPattern:
    return _path(route=route, view=view, kwargs=kwargs, name=name, Pattern=make_pattern)
