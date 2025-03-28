from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("api/v1/", include("api.urls")),
    path("captcha/", include("captcha.urls")),
    path("", include("main.urls")),
    path("", include("feedback.urls")),
    path("", include("articles.urls")),
    path("", include("comments.urls")),
    path("search/", include("search.urls")),
    path("auth/", include("authentication.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls))
    ]
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
