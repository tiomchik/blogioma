from django.views.decorators.cache import cache_page
from django.urls import path

from . import views

urlpatterns = [
    path("sign_up/", views.SignUp.as_view(), name="sign_up"),
    path("login/", views.Login.as_view(), name="log_in"),
    path("logout/", views.logout, name="logout"),

    path("profile/<str:username>/", views.profile, name="profile"),
    path(
        "profile/<str:username>/settings/", views.profile_settings,
        name="profile_settings"
    ),
    path(
        "profile/<str:username>/settings/social_media_links/",
        cache_page(60 * 60)(views.SocialMediaLinks.as_view()),
        name="social_media_links"
    ),

    path(
        "change_username/",
        views.ChangeUsername.as_view(),
        name="change_username"
    ),
    path(
        "change_password/",
        views.ChangePassword.as_view(),
        name="change_password"
    ),
    path(
        "change_pfp/", cache_page(60 * 60)(views.ChangePfp.as_view()),
        name="change_pfp"
    ),
]
