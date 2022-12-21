from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.utils.text import slugify

from django.db.models.signals import pre_save


from .utils.utils import *

from django.core.mail import send_mail
from multiselectfield import MultiSelectField

from django.contrib.auth.models import AbstractUser

# Create your models here.
# Author's profile
class Profile(models.Model):
    authorName = models.CharField(max_length=200)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    profile_image = models.ImageField(
        blank=True, upload_to='profile/images', validators=[valid_image, valid_image_mimetype, valid_size])

    about_me = models.TextField(blank=True, null=True)

    country = models.CharField(max_length=30, null=True)

    genre = models.ManyToManyField('novel.Genre')

    twitter = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.user}"


class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    favorite = models.ManyToManyField('novel.Novel', blank=True)
    saved_novels = models.ManyToManyField(
        'Novel', blank=True,  related_name='saved_novel')
    saved_audios = models.ManyToManyField(
        'Audio', blank=True,  related_name='saved_audios')
    recently_viewed_chapters = models.ManyToManyField(
        'Chapters', blank=True, related_name='recently_viewed_chapters')
    recently_viewed_audios = models.ManyToManyField(
        'Audio', blank=True,  related_name='recently_viewed_audios')
    saved_poems = models.ManyToManyField(
        'Poems', blank=True, related_name='saved_poems')
    last_searched = models.CharField(
        max_length=200, blank=True, unique=True, null=True )
    is_author = models.BooleanField(default=False)
    has_interest = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    def mail_user(self, subject: str, message: str, html_message: str = None) -> None:
        send_mail(subject, message,  "reply.seehowtv@gmail.com" [
                  self.email], fail_silently=False, html_message=html_message)



# ...

MY_CHOICES1 = ((1, 'Traveling'),
               (2, 'Reading'),
               (3, 'Singing'),
               (4, 'Dancing'),
               (5, 'Movies'))

MY_CHOICES2 = ((1, 'Action'),
               (2, 'Adventure'),
               (3, 'Comedy'),
               (4, 'Romance'),
               (5, 'Fantasy'))

MY_CHOICES3 = (
    (1, 'Spanish'),
    (2, 'English'),
    (3, 'Yoruba'))

MY_CHOICES4 = (
    (1, 'Author'),
    (2, 'Reader')
)
MY_CHOICES5 = (
    (1, 'Medieval'),
    (2, 'Cyberpunk'),
    (3, 'Iceage'),
    (4, 'Ile-ife dynasty'),
    (5, 'Neolitic'),
    (6, 'Northern Caliphate'),
    (7, 'Paleolithic')
)
MY_CHOICES6 = (
    (1, 'Women'),
    (2, 'Men'),
    (3, 'GenZ'),
    (4, 'Ile-ife dynasty'),
    (5, 'Neolitic'),
    (6, 'Northern Caliphate'),
    (7, 'Paleolithic')
)
MY_CHOICES7 = (
    (1, 'Christain'),
    (2, 'Muslim'),
    (3, 'Judaism'),
    (4, 'Ile-ife dynasty'),
    (5, 'Neolitic'),
    (6, 'Northern Caliphate'),
    (7, 'Paleolithic')
)


class UserIntrest(models.Model):
    user = models.OneToOneField('User', on_delete=models.CharField)
    hobbies = MultiSelectField(choices=MY_CHOICES1, max_choices=3, blank=True)
    genre = MultiSelectField(choices=MY_CHOICES2, blank=True,
                             max_length=3)
    profile = MultiSelectField(choices=MY_CHOICES4, blank=False, max_choices=1)
    language = MultiSelectField(choices=MY_CHOICES3, blank=True,
                                max_length=3)
    history = MultiSelectField(choices=MY_CHOICES5, blank=True, max_length=3)
    identity = MultiSelectField(choices=MY_CHOICES6, blank=True,
                                max_choices=3,
                                max_length=3)
    faith = MultiSelectField(choices=MY_CHOICES7, blank=True,
                                max_choices=3,
                                max_length=3)



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
        'Profile', related_name='profile', on_delete=models.SET_NULL, blank=True, null=True)

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
        'Profile', on_delete=models.SET_NULL, blank=True, null=True)

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
        'Profile', on_delete=models.SET_NULL, blank=True, null=True)

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


