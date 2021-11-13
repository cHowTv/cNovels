from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model



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
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"password field didnt match"})
        return attrs


    def create(self, validated_data):
        user  =  User.objects.create(
            email = validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        redis_client.incr("total_users")
        user_key = f"user:{user.id}"
        username_key = f"username:{user.username}"
        #added user to redis for chat
        redis_client.set(user_key, username_key)


        return user 