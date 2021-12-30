from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import magic
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from rest_framework.exceptions import bad_request
from star_ratings.models import Rating
import sys
from django.utils.text import slugify
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions  import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
valid_file = FileExtensionValidator (allowed_extensions=['pdf', 'doc', 'docx' ])
valid_image = FileExtensionValidator(allowed_extensions=['jpeg','png', 'jpg'])

def get_mime(value):
    mime = magic.Magic(mime=True)
    mimetype =  mime.from_buffer(value.read(2048))
    value.seek(0)
    return mimetype

def valid_size(value):
    filesize = value.size
    if filesize > 1* 1024 * 1024:
         raise ValidationError('The maximum file size that can be uploaded is 1MB')
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
    if 'pdf' or'msword' or'document' in mimetype : 
        return value
    else:
        return ValidationError('This Field accept only book format')

def compress (bookImage):
    im = Image.open(bookImage)
    im_io = BytesIO()
    im = im.resize((179,209 ))
    im = im.convert('RGB')
    im.save(im_io, 'JPEG', quality=90)
    im_io.seek(0)
    bookImage = InMemoryUploadedFile(im_io,'ImageField', '%s.jpg' % bookImage.name.split('.')[0], 'image/jpeg',sys.getsizeof(im_io), None)
    return bookImage


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200,
     help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"

class Chapters(models.Model):
    title = models.CharField(max_length=200,blank=True,unique=True, null=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    book = RichTextField(config_name='novellas')
    novel = models.ForeignKey('Novel',related_name='books', on_delete=models.SET_NULL,blank=True, null=True)

def validate_chapter(sender, instance, **kwargs):
    instance.number = Chapters.objects.count()+1



pre_save.connect(validate_chapter, sender=Chapters)


class Novel(models.Model):

    title = models.CharField(max_length=200,blank=True,unique=True, null=True)

    slug = models.SlugField(max_length=200,unique=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Profile',related_name='profile', on_delete=models.SET_NULL,blank=True, null=True)

    premium = models.BooleanField(default=False)
    
    #Summary of the book 
    summary = RichTextField()

    isbn = models.CharField( max_length=13,unique=True, null=True, blank=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number </a>')

# ManyToManyField used because genre can contain many books. EBooks can cover many genres.
# Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select multiple genres for this book')
    
    #if authors were to upload books if already written
    #will be parsed and restored into chapters later  
    #bookFile = models.FileField(blank=True,upload_to='book_files/' , validators= [valid_file,valid_pdf_mimetype,valid_size],null=False)
    

    date_uploaded = models.DateField(default = timezone.now)

    bookImage = models.ImageField(null=True, blank=True, upload_to='book/images/', validators= [valid_image,valid_image_mimetype,valid_size]) 
    
    created_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True, related_name='created')
    
    ratings = GenericRelation(Rating, related_query_name='novels_ratings')

    readers_num = models.IntegerField(blank=True, null=True)

    

    def save(self, *args,  **kwargs ):
        self.slug = slugify(self.title)
        super(Novel, self).save(*args, **kwargs)


#use django signal for save  


    
    def __str__(self):
        return f"{self.title}"



class Poems(models.Model):
     title = models.CharField(max_length=200,blank=True,unique=True, null=True)

     slug = models.SlugField(max_length=200,unique=True)
    
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
     author = models.ForeignKey('Profile', on_delete=models.SET_NULL,blank=True, null=True)
    
     premium = models.BooleanField(default=False)

     isbn = models.CharField( max_length=13,unique=True, null=True, blank=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number </a>')
     
     #if authors were to upload books if already written
     #will be parsed and restored into chapters later  
     bookFile = models.FileField(blank=False,upload_to='book_files/' , validators= [valid_file,valid_pdf_mimetype,valid_size])
     
     #if authors were to write instead of upload
     story = RichTextField(config_name='novellas')

     date_uploaded = models.DateField(default = timezone.now)

     bookImage = models.ImageField(default ='default_profile.jpg', upload_to='book/images/', validators= [valid_image,valid_image_mimetype,valid_size]) 
     
     created_author = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True, related_name='poemcretor')
     
     ratings = GenericRelation(Rating, related_query_name='poems_ratings')




    
  

     def save(self, *args, **kwargs):
         
        self.bookImage = compress(self.bookImage)
        super(Novel, self).save( *args,**kwargs )

        
     def __str__(self):
        return f"{self.title}"


# Author's profile 
class Profile(models.Model):
    authorName = models.CharField(max_length=200)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    
    profile_image = models.ImageField(blank=True, upload_to='profile/images' , validators = [valid_image,valid_image_mimetype,valid_size])   

    about_me = models.TextField(blank=True, null=True)

    country = models.CharField(max_length=30, null=True)

    genre = models.ManyToManyField(Genre)

    twitter = models.CharField(max_length=30, null=True)

    


    def __str__(self):
        return f"{self.user}"

class UserBook(models.Model):
    STATUS_UNREAD = 'u'
    STATUS_READ = 'r'
    STATUS_CHOICES = [
        (STATUS_UNREAD, 'unread'),
        (STATUS_READ, 'read'),
    ]
    book = models.ForeignKey(Novel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_UNREAD)

    
class Audio(models.Model):

    title = models.CharField(max_length=200,blank=True,unique=True, null=True)

    slug = models.SlugField(max_length=200,unique=True)
# Foreign Key used because book can only have one author, but authors can have multiple books
# Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL,blank=True, null=True)

    premium = models.BooleanField(default=False)
    
    #Summary of the book 
    summary = RichTextField()

# ManyToManyField used because genre can contain many books. EBooks can cover many genres.
# Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select multiple genres for this book')
    
    #if authors were to upload books if already written
    #will be parsed and restored into chapters later  
    bookFile = models.FileField(blank=False,upload_to='book_files/' , validators= [valid_file,valid_pdf_mimetype,valid_size])

    date_uploaded = models.DateField(default = timezone.now)

#verify and default save later
    bookImage = models.FileField(default ='default_profile.jpg', upload_to='book/images/', validators= [valid_image,valid_image_mimetype,valid_size]) 
    
    created_author = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True, related_name='audiocreator')
    
    ratings = GenericRelation(Rating, related_query_name='audio_ratings')

    




    
  

    def save(self, *args, **kwargs):
         
        self.bookImage = compress(self.bookImage)
        super(Novel, self).save( *args,**kwargs )

        
    def __str__(self):
        return f"{self.title}"


# Extends User model
from multiselectfield import MultiSelectField

# ...

MY_CHOICES = ((1, 'Traveling'),
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

class UserIntrest(models.Model):
    user = models.OneToOneField('User', on_delete=models.CharField)
    hobbies = MultiSelectField(choices=MY_CHOICES, blank=True)
    genre = MultiSelectField(choices=MY_CHOICES2,blank=True,
                                 max_choices=3,
                                 max_length=3)
    language = MultiSelectField(choices=MY_CHOICES3,blank=True,
                                 max_choices=3,
                                 max_length=3)



class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    favorite = models.ManyToManyField(Novel,blank=True)
    saved_novels = models.ManyToManyField(Novel,blank=True ,  related_name='saved_novel')
    saved_audios =  models.ManyToManyField(Audio,blank=True,  related_name='saved_audios')
    recently_viewed_chapters = models.ManyToManyField(Chapters, blank=True, related_name='recently_viewed_chapters')
    recently_viewed_audios = models.ManyToManyField(Audio,blank=True,  related_name='recently_viewed_audios')
    saved_poems = models.ManyToManyField(Poems,blank=True , related_name='saved_poems')
    last_searched = models.CharField(max_length=200,blank=True,unique=True, null=True)
    is_author = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.username
#weekly shoutouts , these should be based on "most rated" 

class Weekly(models.Model):
    novels_of_week = models.ForeignKey(Novel,blank=True, on_delete=models.CASCADE, related_name='weeknovel')
    poems_of_week = models.ForeignKey(Poems,blank=True, on_delete=models.CASCADE, related_name='weekpoems')
    audios_of_week = models.ForeignKey(Audio,blank=True, on_delete=models.CASCADE, related_name='weekaudios')
    special_feature = models.ForeignKey(Novel,blank=True, on_delete=models.CASCADE, related_name='weekspecial')
    authors_of_week = models.ForeignKey(Profile,blank=True, on_delete=models.CASCADE, related_name='weekauthors')
    def __str__(self):
        return f"{self.novels_of_week}"

class Room(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User,related_name='admins' )
    name = models.CharField(max_length=100, unique=True)
    discription = models.TextField()
    private = models.BooleanField(default=False)


class RoomMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateField()



class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')        
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')        
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)



class Event(models.Model):
    name = models.CharField(max_length=100)
    time  = models.DateField()

    def __str__(self):
        return self.name

        

class GroupChat(models.Model):
    citizens = models.ManyToManyField(User)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    event = models.ForeignKey(Event,null=True,blank=True, on_delete=models.SET_NULL)



    def __str__(self) :
        return f'group {self.room.name}'

