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
from django.db.models import Count
from django_countries.fields import Country


def index(request):

    return render(request, "core/index.html")


def signup_view(request):

    if request.method == "POST":

        email = request.POST.get("email").lower()
        first_name = request.POST["first_name"]
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        country = request.POST.get('country')
        referee_code = request.POST.get('referee_code')

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
        user.profile.referee_code = referee_code
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

    # COUNTRIES OF PROFILES IN LOBBY
    # 1. Aggregate the profile count by the country code
    # We filter out any profiles where the country might be blank/null
    country_counts_queryset = Profile.objects.exclude(country__isnull=True).exclude(country='').values('country').annotate(
        count=Count('country')
    ).order_by('-count')  # Order by count, descending

    # 2. Convert the list of dictionaries to a list of tuples containing
    # (Country object, count) for easier access in the template.
    country_stats = []
    for item in country_counts_queryset:
        country_code = item['country']
        profile_count = item['count']

        # Create a Country object from the code using django-countries utility
        country_object = Country(country_code)

        country_stats.append((country_object, profile_count))

    count = Lobby.objects.count()
    return render(request, "core/lobby.html", {"count": count, "country_stats": country_stats})


@login_required
def album_voting(request):

    return render(request, "core/album_voting.html")


@login_required
def referral(request):
    profile = getattr(request.user, "profile", None)
    referral_code = getattr(profile, "referral_code", None)
    link = "https://beymore.up.railway.app"

    return render(request, "core/referral.html", {
        "referral_code": referral_code,
        "link": link,
    })
