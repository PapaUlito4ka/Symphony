from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

import artist.admin as artist_admin
import artist.models as artist_models
import user.admin as user_admin
import user.models as user_models
from artist.formviews import SignUpView


class CustomAdminSite(admin.AdminSite):
    site_header = _('Artist panel')
    site_title = _('Artist panel')

    def get_urls(self):
        return [
            path('sign-up/', SignUpView.as_view(), name='sign-up',)
        ] + super().get_urls()


admin_site = CustomAdminSite(name='Custom admin')
# User admin
admin_site.register(user_models.User, user_admin.UserAdmin)
admin_site.register(user_models.UserProfile, user_admin.UserProfileAdmin)
admin_site.register(user_models.Playlist, user_admin.PlaylistAdmin)
# Artist admin
admin_site.register(artist_models.Artist, artist_admin.ArtistAdmin)
admin_site.register(artist_models.ArtistProfile, artist_admin.ArtistProfileAdmin)
admin_site.register(artist_models.Album, artist_admin.AlbumAdmin)
admin_site.register(artist_models.Song, artist_admin.SongAdmin)
admin_site.register(artist_models.MusicType, artist_admin.MusicTypeAdmin)
