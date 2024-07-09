from django.contrib import admin
from django.conf import settings
from django.urls import include
from django.conf.urls.static import static

from main.utils import my_path

urlpatterns = [
    my_path("api/v1/", include("api.urls")),
    my_path("captcha/", include("captcha.urls")),
    my_path("", include("main.urls")),
    my_path("", include("feedback.urls")),
    my_path("", include("articles.urls")),
    my_path("", include("comments.urls")),
    my_path("search/", include("search.urls")),
    my_path("auth/", include("authentication.urls")),
    my_path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        my_path("__debug__/", include(debug_toolbar.urls))
    ]
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
