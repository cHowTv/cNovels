from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Genre

User = get_user_model()


#creates new genre

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
