from rest_framework import serializers
from .models import NovelModel, ChapterModel


class NovelSerializer(serializers.ModelSerializer):

    class Meta:
        model = NovelModel
        fields = ['title', 'image', 'author__name']



class ChapterSerializer(serializers.ModelSerializer):
    book = NovelSerializer()
    class Meta:
        model = ChapterModel
        fields = '__all__'