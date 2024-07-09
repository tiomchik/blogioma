from . import views
from .utils import my_path

urlpatterns = [
    my_path("", views.Home.as_view(), name="home"),
    my_path("about/", views.about, name="about"),
]
