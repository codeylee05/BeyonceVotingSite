from .models import Album, Vote, Profile
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Lobby, Profile, Album, Vote
from django_countries import countries
from django.db.models import F
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django_countries.fields import Country
from django.http import JsonResponse
from django.utils import timezone


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

    country_counts_queryset = Profile.objects.exclude(country__isnull=True).exclude(country='').values('country').annotate(
        count=Count('country')
    ).order_by('-count')  # Order by count, descending

    country_stats = []
    for item in country_counts_queryset:
        country_code = item['country']
        profile_count = item['count']

        country_object = Country(country_code)

        country_stats.append((country_object, profile_count))

    count = Lobby.objects.count()
    return render(request, "core/lobby.html", {"count": count, "country_stats": country_stats})


@login_required
def album_voting(request):

    albums = Album.objects.all()

    return render(request, "core/album_voting.html", {
        "albums": albums})


@login_required
def referral(request):
    profile = getattr(request.user, "profile", None)
    referral_code = getattr(profile, "referral_code", None)
    link = "https://beymore.up.railway.app"

    return render(request, "core/referral.html", {
        "referral_code": referral_code,
        "link": link,
    })


@login_required
def account_view(request):

    user = request.user
    profile = getattr(user, "profile", None)
    return render(request, "core/account.html", {
        "user": user,
        "profile": profile,
    })

# Removed for now


@login_required
def queens_circle(request):

    badge_holders = Profile.objects.filter(has_badge=True)
    return render(request, 'core/queens_circle.html', {'badge_holders': badge_holders})


# ------------------Voting Logic -----------------


def can_user_vote(user):

    today = timezone.now().date()
    profile = user.profile  # assuming OneToOne relationship
    daily_limit = profile.daily_vote_limit

    votes_today = Vote.objects.filter(user=user, date=today).count()
    return votes_today < daily_limit


def can_user_vote(user):

    daily_limit = 2 if user.profile.has_badge else 1
    today = timezone.now().date()
    votes_today = Vote.objects.filter(user=user, date=today).count()
    return votes_today < daily_limit


def can_vote_for_album(user, album):

    today = timezone.now().date()
    if Vote.objects.filter(user=user, album=album, date=today).exists():
        return False
    return can_user_vote(user)


def vote_album(request, album_id):
    """
    Handle AJAX vote request.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'You must be logged in to vote.'})

    album = get_object_or_404(Album, pk=album_id)
    user = request.user

    if not can_vote_for_album(user, album):
        return JsonResponse({'success': False, 'message': 'Oopps! You cannot vote for this album today. See the rules'})

    Vote.objects.create(user=user, album=album)
    return JsonResponse({'success': True, 'message': 'Slay! Your vote has been recorded! Come back tomorrow to vote again. Note: Queens Circle Members can vote twice daily but for different albums'})


# Ranking Page
def album_ranking(request):

    albums = Album.objects.annotate(votes=Count('vote')).order_by('-votes')
    return render(request, 'core/album_ranking.html', {'albums': albums})
