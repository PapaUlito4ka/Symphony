from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest


class ArtistAdmin(UserAdmin):
    list_display = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_confirmed', 'is_superuser')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_queryset(self, request: HttpRequest):
        user = request.user
        if not user.is_superuser:
            return self.model.objects.filter(id=user.id)
        return super(ArtistAdmin, self).get_queryset(request)

    def get_list_display(self, request):
        list_display = ['email']
        if request.user.is_superuser:
            list_display.extend(['is_staff', 'is_active'])
        return list_display

    def get_list_filter(self, request):
        return self.get_list_display(request)

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ('email',)}),
        ]
        if request.user.is_superuser:
            fieldsets.append(
                ('Permissions', {'fields': ('is_staff', 'is_active', 'is_confirmed', 'is_superuser')})
            )

        # TODO: email confirmation on change
        return fieldsets

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ArtistProfileAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest):
        user = request.user
        if not user.is_superuser:
            return self.model.objects.filter(artist=user)
        return super(ArtistProfileAdmin, self).get_queryset(request)

    def has_add_permission(self, request: HttpRequest):
        return request.user.is_superuser

    def has_delete_permission(self, request: HttpRequest, obj=None):
        return request.user.is_superuser

    def get_exclude(self, request, obj=None):
        return [] if request.user.is_superuser else ('artist',)


class AlbumAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest):
        user = request.user
        if not user.is_superuser:
            return self.model.objects.filter(artists__in=[user])
        return super(AlbumAdmin, self).get_queryset(request)


class SongAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request: HttpRequest):
        user = request.user
        if not user.is_superuser:
            return self.model.objects.filter(album__artists__in=[user])
        return super(SongAdmin, self).get_queryset(request)


class MusicTypeAdmin(admin.ModelAdmin):
    pass

