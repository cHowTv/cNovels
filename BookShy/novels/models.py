from django.db import models

from authors.models import AuthorModel

# Create your models here.
class NovelModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE, related_name='books')


class ChapterModel(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(NovelModel, on_delete=models.CASCADE, related_name='chapters')
 