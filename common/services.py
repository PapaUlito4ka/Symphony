from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile, TemporaryUploadedFile


def resize_image(image: UploadedFile, width=160):
    img_io = BytesIO()
    img = Image.open(image)
    img = ImageOps.exif_transpose(img)
    percent = (width / float(img.size[0]))
    hsize = int(float(img.size[1]) * percent)
    img = img.resize((width, hsize), Image.ANTIALIAS)

    img.save(img_io, format=image.content_type.split('/')[1])

    if isinstance(image, TemporaryUploadedFile):
        return InMemoryUploadedFile(
            img_io,
            'field_name',
            image.name,
            image.content_type,
            image.size,
            image.charset
        )
    return InMemoryUploadedFile(
        img_io,
        image.field_name,
        image.name,
        image.content_type,
        image.size,
        image.charset
    )
