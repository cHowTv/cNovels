from django.db import models

from authors.models import AuthorModel

# Create your models here.
class NovelModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE, related_name='books')
    readers_num = models.IntegerField(blank=True, null=True)
    image = models.ImageField()
    weekly_featured = models.BooleanField(default=False)
    special_featured = models.BooleanField(default=False)
    pubished = models.BooleanField(default=True)
    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    

    class Meta():
        ordering = ["-date_uploaded"]


    def __str__(self) -> str:
        return self.title
    

class ChapterModel(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(NovelModel, on_delete=models.CASCADE, related_name='chapters')
    date_uploaded = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    



 


