from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserIntrest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils.choices import *
from .utils.mailer import verification_email

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['profile'] = user.userintrest.profile[0]
        token['has_interest'] = user.has_interest
        return token

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        user  =  User.objects.create(
            email = validated_data['email'],
            username = validated_data['username']

        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        subject, message = verification_email(user)    
        user.email_user(subject, message, html_message = message)
        return user

    class Meta:
        model = User
        fields = ('username', "email", "password")


class InterestSerializers(serializers.Serializer):
    hobbies = serializers.MultipleChoiceField(
                        choices = HOBBIES)
    genre = serializers.MultipleChoiceField(
                        choices = GENRE)
    language = serializers.MultipleChoiceField(
                        choices = LANGUAGE)
    profile = serializers.MultipleChoiceField(
                        choices = PROFILE)
  
    identity = serializers.MultipleChoiceField(
                        choices = IDENTITY
    )
    faith = serializers.MultipleChoiceField(
                        choices = FAITH
    )
    history = serializers.MultipleChoiceField(
        choices = HISTORY
    )

    def create(self, validated_data):
        if self.context["request"].user.has_interest:
            raise serializers.ValidationError("User Already Registered Intrest.")
        user_attributes = UserIntrest.objects.create(**validated_data)
        self.context["request"].user.has_interest = True
        self.context["request"].user.save()
        return user_attributes

