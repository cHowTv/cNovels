from django.db import models
from django.conf import settings

# Create your models here.

class AuthorModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=23, db_index=True)
    




