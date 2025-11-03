from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("", views.index, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home", views.home_view, name="home"),
    path("lobby/join/", views.join_lobby, name="join_lobby"),
    path("lobby/", views.lobby, name="lobby"),
    path("voteforalbum/", views.album_voting, name="album_voting"),
    path("share/", views.referral, name="referral"),
    path("account/", views.account_view, name="account"),
    path('queens-circle/', views.queens_circle, name='queens_circle'),
    path('vote/<int:album_id>/', views.vote_album, name='vote_album'),
    path('album-ranking/', views.album_ranking, name='album_ranking'),
    path("non-voters/", views.non_voters_list, name="non_voters"),



    # Auth-views for password reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='core/password_reset.html',
             email_template_name='registration/password_reset_email.html'  # the email sent
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/password_reset_complete.html'),
         name='password_reset_complete'),



]
