from django.urls import path

from . import views

urlpatterns = [
    path("sign_up/", views.SignUp.as_view(), name="sign_up"),
    path("login/", views.Login.as_view(), name="log_in"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path(
        "change_username/", views.ChangeUsername.as_view(),
        name="change_username"
    ),
    path(
        "change_password/", views.ChangePassword.as_view(),
        name="change_password"
    ),
    path("change_pfp/", views.ChangePfp.as_view(), name="change_pfp"),

    # Profile
    path("profile/<str:username>/", views.see_profile, name="see_profile"),
    path(
        "profile/<str:username>/settings/", views.profile_settings,
        name="profile_settings"
    ),
]
