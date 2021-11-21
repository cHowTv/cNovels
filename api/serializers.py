from django.contrib.auth.models import  Group
from django.contrib.contenttypes import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from novel.models import *

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","last_searched","recently_viewed_novels","saved_novels"]




class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class WeeklySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekly
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        exclude = ['bookFile',]

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude= ['bookFile',]

class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poems
        exclude =  ['bookFile', 'story']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = '__all__'

class UserNovelSerializer(serializers.ModelSerializer):
    book = NovelSerializer(read_only=True)
    class Meta:
        model = UserBook
        exclude = ('user',)
        depth = 2
    def update(self, instance, validated_data):
        data = validated_data.pop('state')
        print(validated_data)
        instance.state= data
        instance.save()
        return instance
        