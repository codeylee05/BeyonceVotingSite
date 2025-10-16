# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='Select country')

    def __str__(self):

        return f"{self.user.username} - {self.country.name if self.country else 'No country'}"


class Lobby(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="lobby_entry"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} in lobby"
