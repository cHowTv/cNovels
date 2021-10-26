from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers
from .models import GroupChat, Message

User = get_user_model()
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False,read_only=True, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False,read_only=True, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        models = GroupChat
        fields = '__all__'
