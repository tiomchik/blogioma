from main.utils import my_path
from . import views

urlpatterns = [
    my_path("", views.Search.as_view(), name="search"),
    my_path("<str:query>/", views.search_results, name="search_results"),
]
