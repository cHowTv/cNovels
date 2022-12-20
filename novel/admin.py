from django.conf import UserSettingsHolder
from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from api.models import Event, Message, Room, GroupChat

from user.models import Profile, UserIntrest, User



from .models import Audio, Chapters, Genre, Novel, Poems, Weekly, UserBook

admin.site.register(User)
admin.site.register(Weekly)
admin.site.register(Novel)
admin.site.register(Genre)
admin.site.register(Chapters)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(GroupChat)
admin.site.register(Event)
admin.site.register(UserBook)
admin.site.register(Audio)
admin.site.register(Poems)
admin.site.register(UserIntrest)
