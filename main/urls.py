from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("about/", about, name="about"),
    
    # Feedback
    path("feedback/", Feedback.as_view(), name="feedback"),
    path("article/<int:pk>/report/", ReportArticle.as_view(), 
                                                name="report"),

    # Authentication
    path("sign_up/", SignUp.as_view(), name="sign_up"),
    path("login/", Login.as_view(), name="log_in"),
    path("logout_user/", logout_user, name="logout_user"),
    path("change_username/", ChangeUsername.as_view(),
                                        name="change_username"),
    path("change_password/", ChangePassword.as_view(),
                                        name="change_password"),
    path("change_pfp/", ChangePfp.as_view(),
                                        name="change_pfp"),

    # Articles
    path("add_article/", AddArticle.as_view(), name="add_article"),
    path("article/<int:pk>/", ReadArticle.as_view(), name="read"),
    path("article/<int:pk>/delete/", delete_article,
                                                    name="delete"),
    path("article/<int:pk>/update/", UpdateArticle.as_view(), 
                                                name="update"),
    path("article/random/", random_article, name="random_article"),
    path("article/<str:order_by>/", see_all, name="see_all"),

    # Search
    path("search/", Search.as_view(), name="search"),
    path("search/<str:query>/", search_results,
                                            name="search_results"),

    # Comments
    path("article/<int:pk>/comments/", see_comments, name="comments"),
    path("article/<int:pk>/add_comment/", 
        AddComment.as_view(), name="add_comment"),
    path("article/<int:pk>/comments/<int:comment_pk>/delete", 
                            delete_comment, name="delete_comment"),
    path("article/<int:article_pk>/comments/<int:pk>/update",
                                        UpdateComment.as_view(), 
                                            name="update_comment"),

    # Profile
    path("profile/<str:username>/", see_profile, 
                                            name="see_profile"),
    path("profile/<str:username>/settings/", profile_settings, 
                                        name="profile_settings")
]
