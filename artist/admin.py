from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ArtistAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_confirmed', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_confirmed', 'is_superuser')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    # TODO: make different interface for Admin and Artist


class ArtistProfileAdmin(admin.ModelAdmin):
    pass


class AlbumAdmin(admin.ModelAdmin):
    pass


class SongAdmin(admin.ModelAdmin):
    pass


class MusicTypeAdmin(admin.ModelAdmin):
    pass

