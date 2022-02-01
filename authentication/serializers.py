from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from novel.models import MY_CHOICES4, MY_CHOICES5, Profile, UserIntrest, MY_CHOICES, MY_CHOICES2, MY_CHOICES3



User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token

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
    password2 = serializers.CharField(
        write_only = True,
        required = True,
       
    )

    class Meta :
        model = User 
        fields = ('username','email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"password field didnt match"})
        return attrs


    def create(self, validated_data):
        user  =  User.objects.create(
            email = validated_data['email'],
            username = validated_data['username']

        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
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
        if UserIntrest.objects.filter(user=self.context["request"].user).exists():
            raise serializers.ValidationError("User Already exists.")
        user_attributes = UserIntrest.objects.create(**validated_data)
        return user_attributes


class ProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Profile
        exclude = ('user',)