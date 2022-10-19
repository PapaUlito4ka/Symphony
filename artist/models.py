from django.db import models
from django.contrib.auth.models import AbstractUser

from common.mixins import PhotoMixin, DateTimeMixin


class Artist(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=256, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = 'artist'


class ArtistProfile(PhotoMixin, DateTimeMixin):
    artist = models.OneToOneField(to=Artist, null=False, blank=False, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        db_table = 'artist_profile'


class MusicType(models.Model):
    name = models.CharField(max_length=16, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'music_type'


class Album(PhotoMixin, DateTimeMixin):
    artists = models.ManyToManyField(to=Artist, related_name='albums', db_table='artist_album')
    name = models.CharField(max_length=64, null=False, blank=False)
    is_single = models.BooleanField(default=False)
    music_type = models.ForeignKey(to=MusicType, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'album'


class Song(DateTimeMixin):
    album = models.ForeignKey(to=Album, null=False, blank=False, related_name='songs', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False)
    file = models.FileField()

    class Meta:
        db_table = 'song'
