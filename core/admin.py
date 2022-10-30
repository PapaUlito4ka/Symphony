from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.urls import path
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache

import artist.admin as artist_admin
import artist.models as artist_models
import user.admin as user_admin
import user.models as user_models
from artist.formviews import SignUpView


class CustomAdminSite(admin.AdminSite):
    site_header = _('Artist panel')
    site_title = _('Artist panel')

    login_template = 'admin/login.html'

    def get_urls(self):
        return [
            path('sign-up/', self.sign_up, name='sign-up',)
        ] + super().get_urls()

    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        if request.method == "GET" and self.has_permission(request):
            index_path = reverse("admin:index", current_app=self.name)
            return HttpResponseRedirect(index_path)

        from django.contrib.admin.forms import AdminAuthenticationForm
        from django.contrib.auth.views import LoginView

        context = {**self.each_context(request), "title": _("Log in"), "subtitle": None,
                   "app_path": request.get_full_path(), "username": request.user.get_username(),
                   REDIRECT_FIELD_NAME: reverse("admin:index", current_app=self.name)}
        context.update(extra_context or {})

        defaults = {
            "extra_context": context,
            "authentication_form": self.login_form or AdminAuthenticationForm,
            "template_name": self.login_template or "admin/login.html",
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    def sign_up(self, request, extra_context=None):
        if request.method == "GET" and self.has_permission(request):
            index_path = reverse("admin:index", current_app=self.name)
            return HttpResponseRedirect(index_path)

        context = {
            **self.each_context(request),
            "title": _("Sign up"),
            "subtitle": None,
            "app_path": request.get_full_path(),
            "username": request.user.get_username(),
        }
        context.update(extra_context or {})

        request.current_app = self.name
        return SignUpView.as_view(extra_context=context)(request)


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
