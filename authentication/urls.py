from django.views.decorators.cache import cache_page

from main.utils import my_path
from . import views

urlpatterns = [
    my_path(
        "sign_up/", cache_page(60 * 60)(views.SignUp.as_view()),
        name="sign_up"
    ),
    my_path(
        "login/", cache_page(60 * 60)(views.Login.as_view()), name="log_in"
    ),
    my_path("logout_user/", views.logout_user, name="logout_user"),

    my_path("profile/<str:username>/", views.see_profile, name="see_profile"),
    my_path(
        "profile/<str:username>/settings/", views.profile_settings,
        name="profile_settings"
    ),
    my_path(
        "profile/<str:username>/settings/social_media_links/",
        cache_page(60 * 60)(views.SocialMediaLinks.as_view()),
        name="social_media_links"
    ),

    my_path(
        "change_username/",
        cache_page(60 * 60)(views.ChangeUsername.as_view()),
        name="change_username"
    ),
    my_path(
        "change_password/",
        cache_page(60 * 60)(views.ChangePassword.as_view()),
        name="change_password"
    ),
    my_path(
        "change_pfp/", cache_page(60 * 60)(views.ChangePfp.as_view()),
        name="change_pfp"
    ),
]
