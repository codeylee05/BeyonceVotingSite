from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("home", views.home_view, name="home"),

    path("lobby/join/", views.join_lobby, name="join_lobby"),
    path("lobby/", views.lobby, name="lobby"),

    path("voteforalbum/", views.album_voting, name="album_voting"),
]
