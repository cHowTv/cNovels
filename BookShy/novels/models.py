from django.contrib.gis.db import models
from django.contrib.gis.db.models.fields import PolygonField
from authors.models import AuthorModel
from django.conf import settings
from django.urls import reverse

# Create your models here.
class NovelModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE, related_name='books')
    readers_num = models.IntegerField(blank=True, null=True)
    image = models.ImageField()
    weekly_featured = models.BooleanField(default=False)
    special_featured = models.BooleanField(default=False)
    pubished = models.BooleanField(default=True)
    map = models.ForeignKey('MapType',on_delete=models.CASCADE, null=True, blank=True)
    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    

    class Meta():
        ordering = ["-date_uploaded"]


    def __str__(self) -> str:
        return self.title
    

class ChapterModel(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(NovelModel, on_delete=models.CASCADE, related_name='chapters')
    text = models.TextField()
    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    


class MapType(models.Model):
    name = models.CharField(max_length=30)
    

    def get_absolute_url(self):    
        return reverse('points', args=[str(self.novel_id), str(self.id)])
    
    class Meta:
        unique_together = (('name', 'novel'),)

    def __str__(self) -> str:
        return self.name


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = models.PointField()
    claimed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True, blank=True)
    type  = models.ForeignKey(MapType,blank=True,null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    novel = models.ForeignKey(ChapterModel,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Return string representation."""
        return self.name





class Area(models.Model):
    name = models.CharField(max_length=255)
    location = PolygonField()
    description = models.TextField()
    claimed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,null=True, blank=True)
    novel = models.ForeignKey(ChapterModel,on_delete=models.CASCADE, null=True, blank=True)

 


