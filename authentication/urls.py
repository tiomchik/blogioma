from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path(
        "sign_up/", cache_page(60 * 60)(views.SignUp.as_view()),
        name="sign_up"
    ),
    path("login/", cache_page(60 * 60)(views.Login.as_view()), name="log_in"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path(
        "change_username/",
        cache_page(60 * 60)(views.ChangeUsername.as_view()),
        name="change_username"
    ),
    path(
        "change_password/",
        cache_page(60 * 60)(views.ChangePassword.as_view()),
        name="change_password"
    ),
    path(
        "change_pfp/", cache_page(60 * 60)(views.ChangePfp.as_view()),
        name="change_pfp"
    ),

    # Profile
    path("profile/<str:username>/", views.see_profile, name="see_profile"),
    path(
        "profile/<str:username>/settings/", views.profile_settings,
        name="profile_settings"
    ),
    path(
        "profile/<str:username>/settings/social_media_links/",
        cache_page(60 * 60)(views.SocialMediaLinks.as_view()),
        name="social_media_links"
    )
]
