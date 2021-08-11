from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Chapters, Genre, Novel, Profile, User, Weekly

admin.site.register(User)
admin.site.register(Weekly)
admin.site.register(Novel)
admin.site.register(Genre)
admin.site.register(Chapters)
admin.site.register(Profile)