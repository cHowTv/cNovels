
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
#from novel.tokens import account_activation_token
from django.http import HttpResponseForbidden
# Create your views here.

#create login,logout,register view 
#then create front page



#create authors priviledge (user will be able to perform some privilege actions )
def is_author(user):
    return user.is_author 




@login_required(login_url="/login/")
def home(request):
    week = Weekly.objects.all()
    genres  =  Genre.objects.all()
    return render(request, "bookshy/home.html", {"week": week, "genres" : genres})



@login_required(login_url="/login/")
def search(request):
    genres =  Genre.objects.all()
    if request.POST:
        #create search later
        form = Search(request.POST)
        if form.is_valid():
            name =  form.cleaned_data.get('search bar')
            query = Q(author__authorName__icontains = name)
            query.add(Q(title__icontains= name),Q.OR)
            query.add(Q(genre__name__icontains= name),Q.OR)
            ola = Novel.objects.filter(query)
            poems = Poems.objects.filter(query)
            audio = Audio.objects.filter(query)
            #paginate the output
            olah = pagination(request ,  ola  , 9)
            stories = pagination(request, story, 9)
            form = Search()
            context={
                'form': form,
                'books' : ola,
                'poems':poems,
                'audio': audio,  
                'genre':genres,
                'author':author
                
            }

            return render (request,'bookshy/shop.html',context)
    form = Search()
    context={
                'form': form,
                'top' : books,
                'genre':genres,
                'story':stories,
                'author':author
            }
    return render(request,'bookshy/search.html',context)




@login_required(login_url="/login")
def add_genre(request):
    if request.POST:
        form  =  GenreForm(request.POST)
        if form.is_valid():
            form.save()

    return HttpResponseForbidden()
        
    