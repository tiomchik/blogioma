from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blogioma API",
        default_version="v1",
        description="Simple Django blog application (https://github.com/tiomchik/blogioma)",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)
