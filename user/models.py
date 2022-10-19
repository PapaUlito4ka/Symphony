from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.mixins import DateTimeMixin, PhotoMixin


class User(models.Model):
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    friends = models.ManyToManyField(to='User', db_table='user_friend', related_name='friend_set', symmetrical=False)
    followers = models.ManyToManyField(to='User', through='UserFollower', symmetrical=False)
    songs = models.ManyToManyField(to='artist.Song', db_table='user_song')

    class Meta:
        db_table = 'user'


class UserProfile(PhotoMixin, DateTimeMixin):
    user = models.OneToOneField(to=User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    username = models.CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'user_profile'


class UserFollower(models.Model):
    user = models.ForeignKey(to=User, null=False, blank=False, related_name='follower_set', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=User, null=False, blank=False, related_name='follows_set', on_delete=models.CASCADE)
    is_request = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_follower'


class Playlist(PhotoMixin, DateTimeMixin):
    user = models.ForeignKey(to=User, null=False, blank=False, related_name='playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False)
    songs = models.ManyToManyField(to='artist.Song', db_table='playlist_song')

    class Meta:
        db_table = 'playlist'
