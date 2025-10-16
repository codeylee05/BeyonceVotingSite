# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import uuid


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='Select country', blank=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    referral_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.referral_code:
            self.referral_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):

        code = uuid.uuid4().hex[:8].upper()
        while Profile.objects.filter(referral_code=code).exists():
            code = uuid.uuid4().hex[:8].upper()

        return code

    def __str__(self):

        return f"{self.user.username} - {self.country.name if self.country else 'No country'}"


class Lobby(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="lobby_entry"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} in lobby"
