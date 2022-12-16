
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from novel.models import MY_CHOICES6, MY_CHOICES7
from .utiils import verification_email
from drf_spectacular.utils import extend_schema_serializer , OpenApiExample
from novel.models import MY_CHOICES4, MY_CHOICES5, Profile, UserIntrest, MY_CHOICES1, MY_CHOICES2, MY_CHOICES3

from django.contrib.sites.shortcuts import get_current_site

from rest_framework.exceptions import NotAuthenticated , PermissionDenied


User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Login EndPoint',
            description='Login ',
            value={
                
                'email': "ola@gmail.com",
                'password': 'dumbass'
            },
            request_only=True,
            response_only=False,
        ),
    ],    
)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['interest'] = user.has_interest
        return token

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user = User.objects.filter(username=attrs.get("username")).first()
        try:
            verified = user.email_confirmed or user.is_active
        except: 
            verified = False

        if verified and user:
            credentials['username'] = user.username
            return super().validate(credentials)

        elif user and user.check_password(credentials['password']) and not verified:
            # Resend verification Email, generate another token and send
            
            raise NotAuthenticated(detail = 'Email not verified, Redirect to resend email page')
        else:
            # print(inspect.getfullargspec(NotFound))
            raise PermissionDenied(detail='No active account found with the given credentials', code=403)
       
            




@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Registration EndPoint',
            description='Create an account',
            value={
                'username': 'proflamyt',
                'email': "ola@gmail.com",
                'password': 'dumbass'
            },
            request_only=True,
            response_only=False,
        ),
    ],    
)
class RegisterSerializer(serializers.ModelSerializer):
    """
    Register Users 
    
    """
    email  =  serializers.EmailField(
        required = True,
        validators= [UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )
    

    class Meta :
        model = User 
        fields = ('username','email', 'password')



    def create(self, validated_data):
        user  =  User.objects.create(
            email = validated_data['email'],
            username = validated_data['username']

        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        subject, message = verification_email(user)    
        user.email_user(subject, message, html_message=message)
        return user

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Registration EndPoint',
            description='Create an account',
            value={
                'hobbies': [1],
                'genre': [1],
                'language': [1],
                'profile':[1, 2],
                'timeline': [2,2]
            },
            request_only=True,
            response_only=False,
        ),
    ],    
)
class InterestSerializers(serializers.Serializer):
    hobbies = serializers.MultipleChoiceField(
                        choices = MY_CHOICES1)
    genre = serializers.MultipleChoiceField(
                        choices = MY_CHOICES2)
    language = serializers.MultipleChoiceField(
                        choices = MY_CHOICES3)
    profile = serializers.MultipleChoiceField(
                        choices = MY_CHOICES4)
    timeline = serializers.MultipleChoiceField(
                        choices = MY_CHOICES5)
    identity = serializers.MultipleChoiceField(
                        choices = MY_CHOICES6
    )
    faith = serializers.MultipleChoiceField(
                        choices = MY_CHOICES7
    )

    

    

    def create(self, validated_data):
        if self.context["request"].user.has_interest:
            raise serializers.ValidationError("User Already Registered Intrest.")
        user_attributes = UserIntrest.objects.create(**validated_data)
        return user_attributes


class ProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Profile
        exclude = ('user',)

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Registration EndPoint',
            description='Create an account',
            
            value = {
                'refresh_token': " jhbjkxcjknjk.bjknj-njnjkd"
            },
            request_only=True,
            response_only=False,
        ),
    ],    
)
class LogOutSerializer(serializers.Serializer):
    clear_all_token = serializers.BooleanField() 

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=200)
    access =  serializers.CharField(max_length=200)

class RegisterResponseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)