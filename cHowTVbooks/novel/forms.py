from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]
    #these are unnecessary as django performs these validdations before hand 
    #checks if email is already registed 
    def clean_email(self):
        email_data = self.cleaned_data.get('email')
        email_data=email_data.lower()
        if User.objects.filter(email=email_data).exists():
            raise forms.ValidationError("This email already used") #this might also considered an information disclosure
        return email_data
    #checks if passwords are thesame 
    def clean_password(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError('Enter same Password')
        return pass1

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True,
     help_text='Required field.')

    password = forms.CharField(max_length=30, required=True,
     help_text='Required field.', widget=forms.PasswordInput())


#creates new genre

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
