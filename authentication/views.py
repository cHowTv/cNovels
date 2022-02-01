from django.http.response import Http404
from authentication.permissions import AuthorOrReadOnly
from rest_framework import generics, serializers, status, parsers, viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import InterestSerializers, MyTokenObtainPairSerializer, ProfileSerializer, RegisterSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from novel.models import UserIntrest, Profile
from django.contrib.auth import get_user_model
from authentication.tokens import account_activation_token
from django.http import HttpResponseForbidden
User = get_user_model()


# # Create your views here.
# def register(request):

#  #   if request.user is not None and request.user.is_authenticated:
#  #       return render(request,"bookshy/index.html")
#     errors = None
#     if request.method =='POST':
#         form = SignUpForm(request.POST)
      
        
#         if form.is_valid() and form.clean_email() and form.clean_password():
#             ola = form.save(commit=False) #dont save yet i want to change some params
#             ola.is_active = False
#             ola.save()#okay go ahead and save
#             current_site = get_current_site(request)
#             subject = 'Activate Your MySite Account'
#             message = render_to_string('emails/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)

#             messages.success(request, ('Please Confirm your email to complete registration.')) 
#         errors = form.errors
#     form = SignUpForm() 
#     context = {
#         'form':form,
#         'errors': errors
#     }  
   
#     return render(request,"bookshy/register.html",context)



# def activateAccount(request,uidb64, token):
#     if request.GET:
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#              user = None

#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.email_confirmed = True
#             user.save()
#             login(request, user)
#             messages.success(request, ('Your account have been confirmed.'))
#             return redirect('home')
#         else:
#             messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
#             return redirect('home')


# def login_view(request):
#     form = LoginForm(request.POST or None)

#     msg = None
   
#     if request.method == "POST":

#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
 
#                 return redirect("/home")
#             else:    
#                 msg = 'Invalid credentials'    
#         else:
#             msg = 'Error validating the form'    

#     return render(request, "bookshy/login.html", {"form": form, "msg" : msg})
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")



class MyTokenObtainPairView(TokenObtainPairView):
    """
    login by sending a post request containing username and password to login/

    
    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """

    Register with your username, email and password,
    User Wont be able to log in until after verification
    
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client



class UserInterestView(APIView):
    """
    Allows Users to Add interest by using the post request,
     you can also get users' interests by sending a get request
    """
    serializer_class = InterestSerializers
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        try:
            intrest = UserIntrest.objects.get(user=self.request.user)
        except:
            raise Http404
        return intrest
    def get(self, request):
        intrests = self.get_object()
        # serialize the intrests
        serializer = InterestSerializers(intrests)
        return Response(serializer.data)

    def post(self, request):
        # pass request to verify if user already posted
        serializer = InterestSerializers(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Author Profile 
class ProfileViewset(APIView):
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = ProfileSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
   # http_method_names = ['get', 'post', 'patch', 'delete']

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request):
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   


    
    
 