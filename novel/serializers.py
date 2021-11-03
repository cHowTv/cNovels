from django.contrib.auth import get_user_model
from django.contrib.contenttypes import fields
from django.db import models
from rest_framework import serializers
from .models import GroupChat, Message, Room

User = get_user_model()
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False,slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'is_superuser', 'email',
             'is_active',
            'is_staff', 'groups', 'user_permissions'
        )
        extra_kwargs = {
            # For security to hide the password (we can't read it)
            'password': {'write_only': True},
        }

class RoomSerializer(serializers.ModelSerializer):
    creator = CitizenSerializer(read_only=True)
    admins = CitizenSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'
        depth= 2



class GroupMessageSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)
    room = RoomSerializer()
    class Meta:
        model = GroupChat
        fields = '__all__'
        depth = 2
        

        




class RoomJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']



# class JoinGroupSerializer(serializers.ModelSerializer):
#     room = RoomSerializer(write_only=True)

#     class Meta:
#         model = GroupChat
#         fields = ['citizens', 'room']

#     def create(self, validated_data):
#         room = validated_data['room']
#         user = self.context['request'].user
#         ola = GroupChat.objects.filter(room=room)
#         ola.citizens.add(user)
#         ola.save()

#         return ola

class JoinGroupSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=200)
    user_token = serializers.CharField(max_length=200)
    