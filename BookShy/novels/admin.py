from django.contrib import admin

from novels.models import NovelModel, ChapterModel

# Register your models here.

admin.site.register(NovelModel)
admin.site.register(ChapterModel)