from base64 import urlsafe_b64encode
import email
from email.policy import HTTP
import inspect
from os import access
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from novel.models import MY_CHOICES4, MY_CHOICES5, Profile, UserIntrest, MY_CHOICES, MY_CHOICES2, MY_CHOICES3
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAuthenticated , PermissionDenied
from rest_framework import status

User = get_user_model()

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
            # Resend verification Email
            
            raise NotAuthenticated(detail = 'Email not verified')
        else:
            # print(inspect.getfullargspec(NotFound))
            raise PermissionDenied(detail='No active account found with the given credentials')
       
            


    

class RegisterSerializer(serializers.ModelSerializer):
    email  =  serializers.EmailField(
        required = True,
        validators= [UniqueValidator(queryset=User.objects.all())]
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
        confirmation_token = default_token_generator.make_token(user)
        current_site = get_current_site(self.context["request"])
        subject = 'Activate Your MySite Account'
        #actiavation_link = f'{activate_link_url}/user_id={user.i}&confirmation_token={confirmation_token}'
        data = {
            'verification url': reverse('activate', args=[user.pk, confirmation_token], request=self.context["request"])
        }
        
        message = f"{user} a {current_site.domain}  and {urlsafe_b64encode(force_bytes(user.pk))} and {data}"
            
        
        print(message)
        user.email_user(subject, message)
        return user

class InterestSerializers(serializers.Serializer):
    hobbies = serializers.MultipleChoiceField(
                        choices = MY_CHOICES)
    genre = serializers.MultipleChoiceField(
                        choices = MY_CHOICES2)
    language = serializers.MultipleChoiceField(
                        choices = MY_CHOICES3)
    profile = serializers.MultipleChoiceField(
                        choices = MY_CHOICES4)
    timeline = serializers.MultipleChoiceField(
                        choices = MY_CHOICES5)

    

    def create(self, validated_data):
        if self.context["request"].user.has_interest:
            raise serializers.ValidationError("User Already Registered Intrest.")
        user_attributes = UserIntrest.objects.create(**validated_data)
        return user_attributes


class ProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Profile
        exclude = ('user',)


class LogOutSerializer(serializers.Serializer):
    clear_all_token = serializers.BooleanField() 

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=200)
    access =  serializers.CharField(max_length=200)

class RegisterResponseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)