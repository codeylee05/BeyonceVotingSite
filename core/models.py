# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='Select country', blank=True)
    referral_code = models.CharField(max_length=100, blank=True, null=True)
    referee_code = models.CharField(max_length=100, blank=True, null=True)
    has_badge = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.user.username} - {self.country.name if self.country else 'No country'}"


class Lobby(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="lobby_entry"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} in lobby"


class Album(models.Model):

    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Vote(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    # stores the day the vote was made
    date = models.DateField(auto_now_add=True)

    class Meta:
        # prevents voting for same album more than once per day
        unique_together = ('user', 'album', 'date')

    def __str__(self):
        return f"{self.user} → {self.album} on {self.date}"
