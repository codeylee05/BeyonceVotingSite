from django.contrib import admin
from .models import Lobby, Profile, Album, Vote
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html


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
    change_list_template = "admin/votes_by_album.html"

    def get_urls(self):

        urls = super().get_urls()
        custom_urls = [
            path(
                'by-album/',
                self.admin_site.admin_view(self.votes_by_album_view),
                name='votes_by_album',
            ),
        ]
        return custom_urls + urls

    def votes_by_album_view(self, request):

        albums = Album.objects.all().order_by('title')
        data = []
        for album in albums:
            votes = Vote.objects.filter(album=album).select_related('user')
            data.append({
                'album': album,
                'vote_count': votes.count(),
                'voters': [v.user.username for v in votes],
            })

        context = dict(
            self.admin_site.each_context(request),
            data=data,
            title='Votes grouped by Album',
        )
        return TemplateResponse(request, "admin/votes_by_album.html", context)

    def view_by_album_link(self, obj):

        return format_html('<a href="/admin/core/vote/by-album/">View grouped</a>')
    view_by_album_link.short_description = "Grouped View"
