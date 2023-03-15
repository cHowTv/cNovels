from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.conf import settings
from authentication.utils.choices import *

# Create your models here.
class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

    image = models.ImageField(null=True, blank=True)

    favorite = models.ManyToManyField('novels.NovelModel', blank=True)

    saved_novels = models.ManyToManyField(
        'novels.NovelModel', blank=True,  related_name='saved_novel')
    
    recently_viewed_chapters = models.ManyToManyField(
        'novels.ChapterModel', blank=True, related_name='recently_viewed_chapters')
    
    last_searched = models.CharField(
        max_length=200, blank=True, unique=True, null=True )

    has_interest = models.BooleanField(default=False)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email
    


class UserIntrest(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CharField)

    hobbies = MultiSelectField(choices=HOBBIES, max_length=255, max_choices=3, blank=True)

    genre = MultiSelectField(choices=GENRE, blank=True, max_length=255,)
    
    profile = MultiSelectField(choices=PROFILE, blank=False, max_length=255, max_choices=1)

    language = MultiSelectField(choices=LANGUAGE, blank=True, max_length=255,)
    
    history = MultiSelectField(choices=HISTORY, max_length=255, blank=True)

    identity = MultiSelectField(choices=IDENTITY, blank=True, max_length=255,
                                max_choices=3,)
    
    faith = MultiSelectField(choices=FAITH, blank=True, max_length=255,
                                max_choices=3,
                                )