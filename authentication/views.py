from base64 import urlsafe_b64decode
from django.http.response import Http404
from authentication.permissions import AuthorOrReadOnly
from rest_framework import generics, serializers, status, parsers, viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import InterestSerializers, LogOutSerializer, LoginResponseSerializer, MyTokenObtainPairSerializer, ProfileSerializer, RegisterResponseSerializer, RegisterSerializer
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
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils.encoding import force_str
User = get_user_model()
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django_rest_passwordreset.signals import reset_password_token_created
from novel.responses import  ProductXcodeAutoSchema
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


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


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: LogOutSerializer}
))
class logout_user(APIView):
    
    """
    Logs User out By making a post request to /logout/ (note: just an ordinary post request, it logs user out of current session ), 
    the endpoint logs current user out of all session by posting {all-token : true }
    """
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogOutSerializer
    my_tags = ["Authentication"]
    
    def post(self, request, *args, **kwargs):
        if self.request.data.get('clear_all_token'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all current user's refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"}, status= status.HTTP_401_UNAUTHORIZED)


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: LoginResponseSerializer()}
))
class MyTokenObtainPairView(TokenObtainPairView):
    """
    login by sending a post request containing username and password to login/

    
    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    my_tags = ["Authentication"]



@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: RegisterResponseSerializer}
))
class RegisterView(generics.CreateAPIView):
    
    """

    Register with your username, email and password,
    User Wont be able to log in until after verification.
    Send User To Confirm page view
    # Work on resending mail
    
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    my_tags = ["Authentication"]



class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client
    my_tags = ["Authentication"]


# create user interest
@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: InterestSerializers}
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    responses={200: InterestSerializers}
))
class UserInterestView(APIView):
    """
    Allows Users to Add interest by using the post request,
     you can also get users' interests by sending a get request
    """
    serializer_class = InterestSerializers
    permission_classes = (permissions.IsAuthenticated,)
    my_tags = ["Authentication"]
    swagger_schema = ProductXcodeAutoSchema ## -------------

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
            user = request.user
            serializer.save(user = user)
            user.has_interest = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Author Profile 

class ProfileViewset(APIView):
    """
    Create Author's Profile 
    """
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = ProfileSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    my_tags = ['Author']
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

   


    
@method_decorator(name='get', decorator=swagger_auto_schema(
    responses={301: "redirect to /verified-email-page"}
))    
class VerifyAccount(APIView):
    
    """
    Allows Users To be activated after registration , by clicking link sent to their mail . This is used for email verification.
    Returns Interest endpoint to continue 
    """
    permission_classes = (AllowAny,)
    my_tags = ["Authentication"]

    def get(self,request, uidb64, token):
        try:
            uid = uidb64
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
             user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return redirect('/auth/verify')
        return Response('Token is invalid or expired. Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)




# w
class VerifyPageView(APIView):
    permission_classes = (AllowAny,)
    my_tags = ["Authentication"]

    def get(self, request):
        if request.user.is_active:
            return Response ( f'{request.user.email} is Active , Send to login page ')

        return Response("No, user is inactive")