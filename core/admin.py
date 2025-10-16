from django.contrib import admin
from .models import Lobby, Profile


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_at')
    search_fields = ('user__username',)
    ordering = ('-joined_at',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name',
                    'country', 'referral_code', 'referred_by', 'referral_count')
    list_select_related = ('user',)  # optimize queries
    search_fields = ('user__email', 'referral_code')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'


admin.site.register(Profile, ProfileAdmin)
