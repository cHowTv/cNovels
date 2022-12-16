from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
import magic
from io import BytesIO
import sys

valid_file = FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])
valid_image = FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])


def get_mime(value):
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(value.read(2048))
    value.seek(0)
    return mimetype


def valid_size(value):
    filesize = value.size
    if filesize > 1 * 1024 * 1024:
        raise ValidationError(
            'The maximum file size that can be uploaded is 1MB')
    else:
        return value


def valid_image_mimetype(value):
    mimetype = get_mime(value)
    if mimetype.startswith('image'):
        return value
    else:
        raise ValidationError('This Field accept only image')


def valid_pdf_mimetype(value):
    mimetype = get_mime(value)
    if 'pdf' or 'msword' or 'document' in mimetype:
        return value
    else:
        return ValidationError('This Field accept only book format')


def compress(bookImage):
    im = Image.open(bookImage)
    im_io = BytesIO()
    im = im.resize((179, 209))
    im = im.convert('RGB')
    im.save(im_io, 'JPEG', quality=90)
    im_io.seek(0)
    bookImage = InMemoryUploadedFile(im_io, 'ImageField', '%s.jpg' % bookImage.name.split(
        '.')[0], 'image/jpeg', sys.getsizeof(im_io), None)
    return bookImage

