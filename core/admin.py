from .models import Album, Vote, Profile
from django.contrib import admin
from .models import Lobby, Profile, Album, Vote


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_at')
    search_fields = ('user__username',)
    ordering = ('-joined_at',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'has_badge',
                    'country', 'referral_code', 'referee_code')
    list_select_related = ('user',)  #
    search_fields = ('user__email', )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'


admin.site.register(Profile, ProfileAdmin)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'date')
    list_filter = ('date', 'album')
    search_fields = ('user__username', 'album__title')
    ordering = ('-date',)
