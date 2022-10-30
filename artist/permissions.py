from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from artist.models import Album, ArtistProfile, Song, Artist


def artist_permissions():
    content_types = [v for _, v in ContentType.objects.get_for_models(Album, ArtistProfile, Song, Artist).items()]
    return Permission.objects.filter(content_type__in=content_types)
