from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_serializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from novel.responses import ProductXcodeAutoSchema
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from base64 import b64decode
from django.http.response import Http404
from authentication.permissions import AuthorOrReadOnly
from rest_framework import generics, status, parsers
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .utiils import verification_email
from .serializers import EmailSerializer, InterestSerializers, LogOutSerializer, LoginResponseSerializer, MyTokenObtainPairSerializer, ProfileSerializer, RegisterResponseSerializer, RegisterSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from novel.models import UserIntrest, Profile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

User = get_user_model()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user

    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string(
        'email/user_reset_password.html', context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)

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
        return Response({"status": "OK, goodbye"}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    responses={201: LoginResponseSerializer},
)
class MyTokenObtainPairView(TokenObtainPairView):
    """
    login by sending a post request containing username and password to login/


    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    my_tags = ["Authentication"]


@extend_schema(
    responses = {201: RegisterResponseSerializer},
)
class RegisterView(generics.CreateAPIView):

    """
    Register with your username, email and password,
    User Wont be able to log in until after verification.
    Send User To Confirm page view       
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    my_tags = ["Authentication"]


class GoogleLogin(SocialLoginView):
    authentication_classes = []  # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client
    my_tags = ["Authentication"]


# create user interest

class UserInterestView(APIView):
    """
    Allows Users to Add interest by using the post request,
     you can also get users' interests by sending a get request
    """
    serializer_class = InterestSerializers
    permission_classes = (permissions.IsAuthenticated,)
    my_tags = ["Authentication"]
    swagger_schema = ProductXcodeAutoSchema  # -------------

    def get_object(self):
        try:
            intrest: str = UserIntrest.objects.get(user=self.request.user)
        except:
            raise Http404
        return intrest

    @extend_schema(
        responses={200: InterestSerializers},
    )
    def get(self, request):
        """
        Returns user's interest
        """
        intrests: str = self.get_object()
        # serialize the intrests
        serializer = InterestSerializers(intrests)
        return Response(serializer.data)

    @extend_schema(
        responses={201: InterestSerializers},
    )
    def post(self, request):
        # pass request to verify if user already posted
        serializer = InterestSerializers(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='get', decorator=swagger_auto_schema(
    responses={301: "redirect to verified-email-page"}
))
class VerifyAccount(APIView):

    """
    Allows Users To be activated after registration , by clicking link sent to their mail . This is used for email verification.
    Returns Interest endpoint to continue 
    """
    permission_classes = (AllowAny,)
    my_tags = ["Authentication"]

    def get(self, request, uidb64, token):
        try:
            uid = int(b64decode(uidb64).decode('utf8'))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return redirect(f'https://c-novels-frontend.vercel.app/verify-success/{uid}')
        return Response({
            'message': 'Token is invalid or expired. Please request another confirmation email by signing in.'
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifySuccess(APIView):
    """

    Returns User Id to Query if user has beeen verified

    :return Response 200 Ok 

    :raise 400

    :param userid

    """
    permission_classes = (AllowAny,)
    my_tags = ["Authentication"]

    def get(self, request, userid=None):
        if userid:
            return Response({'userId': userid})
        return Response({
            'message': 'Provide user id'
        }, status=status.HTTP_400_BAD_REQUEST)


# w
class VerifyPageView(APIView):
    """

    Check if user is active or not 

    :param userID

    :return 200 ok, user found or not


    """
    permission_classes = (AllowAny | IsAuthenticated,)
    my_tags = ["Authentication"]

    def get(self, request, userid=None):
        user = request.user
        if user.is_anonymous:
            try:
                user = User.objects.get(pk=userid)
            except Exception:
                return Response("Check User Id")
        if user.is_active:
            return Response({
                'message': 'user is Active , Send to login page'
            })

        return Response({
            'message': "No, user is inactive"
        })


class ResendMail(APIView):
    """
    Resend Verification Email 

    """
    serializer_class = EmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.data['email'])

            if user.email_confirmed:
                return Response({
                    'message': 'User is already verified'
                }, status=status.HTTP_200_OK)

            subject, message = verification_email(user)

            user.email_user(subject, message, html_message=message)

            return Response({
                'message': "Check Email For Verification"
            }, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({
                'message': "Invalid Request"
            }, status=status.HTTP_400_BAD_REQUEST)
