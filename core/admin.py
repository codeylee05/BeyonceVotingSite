from django.contrib import admin
from .models import Lobby


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_at')
    search_fields = ('user__username',)
    ordering = ('-joined_at',)
