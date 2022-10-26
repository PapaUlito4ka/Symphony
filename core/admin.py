from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
import re
from functools import update_wrapper
from weakref import WeakSet

from django.apps import apps
from django.conf import settings
from django.contrib.admin import ModelAdmin, actions
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils.decorators import method_decorator
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.common import no_append_slash
from django.views.decorators.csrf import csrf_protect
from django.views.i18n import JavaScriptCatalog

import artist.admin as artist_admin
import artist.models as artist_models
import user.admin as user_admin
import user.models as user_models
from artist.forms import SignUpForm
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

    # @method_decorator(never_cache)
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
