from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Room(models.Model):
    creator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='admins')
    name = models.CharField(max_length=100, unique=True)
    discription = models.TextField()
    private = models.BooleanField(default=False)


class RoomMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateField()


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(
        null=False, blank=False, auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class Event(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.name


class GroupChat(models.Model):
    citizens = models.ManyToManyField(User)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'group {self.room.name}'
