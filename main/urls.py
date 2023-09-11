from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about/", views.about, name="about"),
    
    # Feedback
    path("feedback/", views.Feedback.as_view(), name="feedback"),
    path("article/<int:pk>/report/", 
                    views.ReportArticle.as_view(), name="report"),

    # Authentication
    path("sign_up/", views.SignUp.as_view(), name="sign_up"),
    path("login/", views.Login.as_view(), name="log_in"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("change_username/", views.ChangeUsername.as_view(),
                                        name="change_username"),
    path("change_password/", views.ChangePassword.as_view(),
                                        name="change_password"),
    path("change_pfp/", views.ChangePfp.as_view(),
                                            name="change_pfp"),

    # Articles
    path("add_article/", views.AddArticle.as_view(), name="add_article"),
    path("article/<int:pk>/", views.ReadArticle.as_view(), name="read"),
    path("article/<int:pk>/delete/", views.delete_article,
                                                    name="delete"),
    path("article/<int:pk>/update/", 
                    views.UpdateArticle.as_view(), name="update"),
    path("article/random/", views.random_article, name="random_article"),
    path("article/<str:order_by>/", views.see_all, name="see_all"),

    # Search
    path("search/", views.Search.as_view(), name="search"),
    path("search/<str:query>/", views.search_results,
                                            name="search_results"),

    # Comments
    path("article/<int:pk>/comments/", views.see_comments, name="comments"),
    path("article/<int:pk>/add_comment/", 
        views.AddComment.as_view(), name="add_comment"),
    path("article/<int:pk>/comments/<int:comment_pk>/delete", 
                    views.delete_comment, name="delete_comment"),
    path("article/<int:article_pk>/comments/<int:pk>/update",
            views.UpdateComment.as_view(), name="update_comment"),

    # Profile
    path("profile/<str:username>/", views.see_profile, 
                                            name="see_profile"),
    path("profile/<str:username>/settings/", 
                views.profile_settings, name="profile_settings"),
]
