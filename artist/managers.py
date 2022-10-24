from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class ArtistManager(BaseUserManager):
    """
    Custom artist model manager where email is the unique identifiers
    for authentication instead of artist names.
    """

    def create_user(self, email: str, password: str, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The email field must be set'))
        if not password:
            raise ValueError(_('Password must be set'))
        email = self.normalize_email(email)
        artist = self.model(email=email, **extra_fields)
        artist.set_password(password)
        artist.save()
        return artist

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_confirmed', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
