from django.contrib import auth
from django.contrib.auth.models import  Group
from django.contrib.contenttypes import fields
from django_filters.rest_framework import filters
from rest_framework import serializers
from django.contrib.auth import get_user_model
from novel.models import *
from django.db.models import Sum 

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","last_searched","saved_novels"]




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


class NovelAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['authorName', 'country']

class NovelSerializer(serializers.ModelSerializer):
    author =  NovelAuthorSerializer(read_only=True)
    #ratings = GernericSerializer(read_only=True)
    readers_num = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    date_uploaded = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Novel
        exclude = ('created_author', 'id')
        

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude= ['bookFile',]

class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poems
        exclude =  [ 'story']

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
        instance.state = data
        instance.save()
        return instance
        

class AuthorSerializer(serializers.ModelSerializer):
    most_popular = serializers.SerializerMethodField()
    new = serializers.SerializerMethodField()
    total_books = serializers.SerializerMethodField()
    total_readers = serializers.SerializerMethodField()
    #user =  UserSerializer()
    class Meta:
        model = Profile
        exclude = ('user',)
    def get_most_popular(self, instance):
        books = instance.profile.all().order_by('ratings')[:20]
        return NovelSerializer(books, many=True).data
    def get_new(self, instance):
        books = instance.profile.all().order_by('date_uploaded')[:20]
        return NovelSerializer(books, many=True).data
    
    def get_total_books(self, instance):
        number = instance.profile.count()
        return number
    def get_total_readers(self, instance):
        readers = instance.profile.all().aggregate(num = Sum('readers_num'))
        return readers
