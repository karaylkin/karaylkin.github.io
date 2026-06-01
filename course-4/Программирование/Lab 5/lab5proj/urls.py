from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from polls import views as polls_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include(("polls.urls", "polls"), namespace="polls")),
    path("register/", polls_views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        polls_views.logout_view,
        name="logout",
    ),
    path("", polls_views.index_redirect, name="home"),
]


