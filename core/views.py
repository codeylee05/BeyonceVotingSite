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


'def backfill_profiles(request):
    created_count = 0
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            # create profile
            profile = Profile.objects.create(user=user)
            # generate unique referral code
            profile.referral_code = profile.generate_unique_code()
            profile.save()
            created_count += 1
    return HttpResponse(f"Backfilled {created_count} missing profiles with unique referral codes.")


def index(request):

    return render(request, "core/index.html")


def signup_view(request):

    with transaction.atomic():

        ref_code = request.POST.get('referral_code', '').strip().upper()

        if request.method == "POST":

            email = request.POST.get("email").lower()
            first_name = request.POST["first_name"]
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            country = request.POST.get('country')

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

            profile, created = Profile.objects.get_or_create(user=user)
            user.profile.country = country
            user.profile.save()

            # Handle referral code if provided
            if ref_code:

                try:

                    referrer_profile = Profile.objects.get(
                        referral_code=ref_code)

                    if referrer_profile == user.profile:
                        messages.warning(
                            request, "You cannot use your own referral code.")

                    else:
                        referrer_profile.referral_count = F(
                            'referral_count') + 1
                        referrer_profile.save()

                        # link new user to referrer
                        user.profile.referred_by = referrer_profile
                        user.profile.save()

                except Profile.DoesNotExist:
                    # invalid referral code
                    messages.warning(
                        request, "Referral code does not exist.")

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
