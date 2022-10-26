from django.db import models
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext as _

from common.services import resize_image


class PhotoMixin(models.Model):
    full_photo = models.ImageField(
        upload_to='users_photos/full_photos',
        blank=True,
        verbose_name=_('full photo')
    )
    preview_photo = models.ImageField(
        upload_to='users_photos/full_photos',
        blank=True,
        editable=False,
        verbose_name=_('full photo')
    )

    def save(self, *args, **kwargs):
        if self.full_photo and isinstance(self.full_photo.file, UploadedFile):
            img = resize_image(self.full_photo.file)
            self.preview_photo.save(img.name, img, save=False)
        return super(PhotoMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class DateTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    class Meta:
        abstract = True
