from django.db import models
from django.core.mail import send_mail
from multiselectfield import MultiSelectField
from django.conf import settings
from novel.utils.utils import *

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
        'novel.Novel', blank=True,  related_name='saved_novel')
    saved_audios = models.ManyToManyField(
        'novel.Audio', blank=True,  related_name='saved_audios')
    recently_viewed_chapters = models.ManyToManyField(
        'novel.Chapters', blank=True, related_name='recently_viewed_chapters')
    recently_viewed_audios = models.ManyToManyField(
        'novel.Audio', blank=True,  related_name='recently_viewed_audios')
    saved_poems = models.ManyToManyField(
        'novel.Poems', blank=True, related_name='saved_poems')
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

