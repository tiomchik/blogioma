from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("", include("main.urls")),
    path("", include("feedback.urls")),
    path("", include("articles.urls")),
    path("", include("comments.urls")),
    path("search/", include("search.urls")),
    path("auth/", include("authentication.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls))
    ]
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
