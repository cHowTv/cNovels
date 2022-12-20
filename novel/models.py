from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from rest_framework.exceptions import bad_request
from star_ratings.models import Rating
import sys
from django.utils.text import slugify

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail

from user.models import *

from .utils.utils import *



# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200,
                            help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"


class Chapters(models.Model):
    title = models.CharField(
        max_length=200, blank=True, unique=True, null=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    book = RichTextField(config_name='novellas')
    novel = models.ForeignKey(
        'Novel', related_name='books', on_delete=models.SET_NULL, blank=True, null=True)


def validate_chapter(sender, instance, **kwargs):
    instance.number = Chapters.objects.count()+1


pre_save.connect(validate_chapter, sender=Chapters)


class Novel(models.Model):

    title = models.CharField(
        max_length=200, blank=True, unique=True, null=True)

    slug = models.SlugField(max_length=200, unique=True)


    author = models.ForeignKey(
        'user.Profile', related_name='profile', on_delete=models.SET_NULL, blank=True, null=True)

    premium = models.BooleanField(default=False)


    summary = RichTextField()

    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number </a>')

    genre = models.ManyToManyField(
        Genre, help_text='Select multiple genres for this book')

 
    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)

    bookImage = models.ImageField(null=True, blank=True, upload_to='book/images/',
                                  validators=[valid_image, valid_image_mimetype, valid_size])

    created_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='created')

    ratings = GenericRelation(Rating, related_query_name='novels_ratings')

    readers_num = models.IntegerField(blank=True, null=True)

    def save(self, *args,  **kwargs):
        self.slug = slugify(self.title)
        super(Novel, self).save(*args, **kwargs)


# use django signal for save

    def __str__(self):
        return f"{self.title}"


class Poems(models.Model):
    title = models.CharField(
        max_length=200, blank = True, unique=True, null=True)

    slug = models.SlugField(max_length=200, unique=True)


    author = models.ForeignKey(
        'user.Profile', on_delete=models.SET_NULL, blank=True, null=True)

    premium = models.BooleanField(default=False)

    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number </a>')


    bookFile = models.FileField(blank=True, upload_to='book_files/',
                                validators=[valid_file, valid_pdf_mimetype, valid_size])

    
    story = RichTextField(config_name='novellas')

    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)

    bookImage = models.ImageField(null=True, blank=True, upload_to='book/images/',
                                  validators=[valid_image, valid_image_mimetype, valid_size])

    created_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='poemcretor')

    ratings = GenericRelation(Rating, related_query_name='poems_ratings')


    def __str__(self):
        return f"{self.title}"




class UserBook(models.Model):
    STATUS_UNREAD = 'u'
    STATUS_READ = 'r'
    STATUS_FINISHED = 'f'
    STATUS_CHOICES = [
        (STATUS_UNREAD, 'unread'),
        (STATUS_READ, 'read'),
        (STATUS_FINISHED, 'finished'),
    ]
    book = models.ForeignKey(Novel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    state = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_UNREAD)


class Audio(models.Model):

    title = models.CharField(
        max_length=200, blank=True, unique=True, null=True)

    slug = models.SlugField(max_length=200, unique=True)
# Foreign Key used because book can only have one author, but authors can have multiple books
# Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(
        'user.Profile', on_delete=models.SET_NULL, blank=True, null=True)

    premium = models.BooleanField(default=False)

    # Summary of the book
    summary = RichTextField()

# ManyToManyField used because genre can contain many books. EBooks can cover many genres.
# Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text='Select multiple genres for this book')

    # if authors were to upload books if already written
    # will be parsed and restored into chapters later
    bookFile = models.FileField(blank=True, upload_to='book_files/',
                                validators=[valid_file, valid_pdf_mimetype, valid_size])

    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)

# verify and default save later
    bookImage = models.ImageField(null=True, blank=True, upload_to='book/images/',
                                  validators=[valid_image, valid_image_mimetype, valid_size])

    created_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='audiocreator')

    ratings = GenericRelation(Rating, related_query_name='audio_ratings')

    # def save(self, *args, **kwargs):
    #     if self.bookImage:
    #         self.bookImage = compress(self.bookImage)
    #         super(Novel, self).save( *args,**kwargs )
    #     return None

    def __str__(self):
        return f"{self.title}"



class Weekly(models.Model):
    weekly_featured_novels = models.ManyToManyField(
        Novel, blank=True, related_name='weeknovel')
    weekly_featured_poems = models.ManyToManyField(
        Poems, blank=True,  related_name='weekpoems')
    weekly_featured_audios = models.ManyToManyField(
        Audio, blank=True, related_name='weekaudios')
    special_feature = models.ManyToManyField(
        Novel, blank=True, related_name='weekspecial')
    authors_of_week = models.ManyToManyField(
        Profile, blank=True, related_name='weekauthors')

    def __str__(self):
        return f"{self.weekly_featured_novels}"


