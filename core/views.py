from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Lobby, Profile
from django_countries import countries
from django.db.models import F
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model


def reset_superuser(request):
    User = get_user_model()

    # Define your new credentials
    username = "MasterUser"
    email = "mleefa5002@gmail.com"
    password = "MasterUserIsCool0000"

    # Delete any existing superusers
    User.objects.filter(is_superuser=True).delete()

    # Create a new one
    User.objects.create_superuser(
        username=username, email=email, password=password)

    return HttpResponse("✅ Superuser reset successfully. You can now log in.")


def index(request):

    return render(request, "core/index.html")


def signup_view(request):

    if request.method == "POST":

        email = request.POST.get("email").lower()
        first_name = request.POST["first_name"]
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        country = request.POST.get('country')
        referral_code = request.POST.get('referral_code')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # Use email as username
        user = User.objects.create_user(
            username=email, email=email, first_name=first_name, password=password1)

        user.save()
        # A signal will create the profile automatically

        profile, created = Profile.objects.get_or_create(
            user=user)
        user.profile.country = country
        user.profile.referral_code = referral_code
        user.profile.save()

        messages.success(request, "Account created! Please log in.")

        return redirect("login")

    return render(request, "core/signup.html", {'countries': countries})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username  # we stored email as username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "core/login.html")


def logout_view(request):

    logout(request)
    return redirect("index")


@login_required
def home_view(request):

    return render(request, "core/home.html")


@login_required
def join_lobby(request):

    lobby = Lobby.objects.filter(user=request.user).first()

    if not lobby:
        lobby = Lobby.objects.create(user=request.user)
        messages.success(request, "You have joined the lobby!")
    else:
        messages.info(request, "You are already in the lobby.")
    return redirect("lobby")


@login_required
def lobby(request):

    count = Lobby.objects.count()
    return render(request, "core/lobby.html", {"count": count})


@login_required
def album_voting(request):

    return render(request, "core/album_voting.html")
