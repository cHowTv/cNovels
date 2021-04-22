
from .form import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView

from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
# Create your views here.

#create login,logout,register view 
#then create front page 

def register(request):

 #   if request.user is not None and request.user.is_authenticated:
 #       return render(request,"school/index.html")
    errors = None
    if request.method =='POST':
        form = SignUpForm(request.POST)
      
        
        if form.is_valid() and form.clean_email() and form.clean_password():
            ola = form.save(commit=False) #dont save yet i want to change some params
            ola.is_active = False
            ola.save()#okay go ahead and save
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.')) 
        errors = form.errors
    form = SignUpForm() 
    context = {
        'form':form,
        'errors': errors
    }  
   
    return render(request,"bookshy/register.html",context)



def activateAccount(request,uidb64, token):
    if request.GET:
         try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
   
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
 
                return redirect("/home")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "bookshy/login.html", {"form": form, "msg" : msg})
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


@login_required(login_url="/login/")
def home(request):
    week = Weekly.objects.all()
    genres  =  Genre.objects.all()
    return render(request, "bookshy/home.html", {"week": week, "genres" : genres})
