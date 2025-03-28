from django.urls import ResolverMatch
from functools import lru_cache
from typing import Any

from .celery import app as celery_app

__all__ = ("celery_app",)


def patch_resolver() -> None:
    from django.urls.resolvers import URLResolver

    orig_resolve = URLResolver.resolve
    cached = lru_cache(maxsize=16)(orig_resolve)

    def dispatcher(self: URLResolver, path: str | Any) -> ResolverMatch:
        if isinstance(path, str):
            return cached(self, path)
        return orig_resolve(self, path)

    URLResolver.resolve = dispatcher


patch_resolver()
