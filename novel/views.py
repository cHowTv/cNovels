#join group api

#Create Group
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models import query
from django.http.response import Http404
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import AuthorOrReadOnly, GroupOwners, GroupCreator
from novel.models import GroupChat, Room, RoomMessage
from rest_framework.response import Response
from novel.serializers import JoinGroupSerializer, RoomSerializer, GroupSerializer, UserSerializer
import redis
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()
# Connect to our Redis instance
redis_client = redis.StrictRedis(host='172.26.255.129', 
  port= 6379,
                              #    port=settings.REDIS_PORT,
                               db=0)
#create group 
class GroupCreateAPIView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        
        serializer.save(room__creator= self.request.user, room__admins = 
        [self.request.user], citizens=[self.request.user])
        redis_client.set(f"room:{serializer.id}:name", f"{serializer.room.name}")
        redis_client.sadd(f"user:{self.request.user.id}:rooms", f"{serializer.id}")
      


#Members list Group
class GroupMembersList(RetrieveAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self,room):
       # room = self.request.data.get('room')
        query = get_object_or_404(GroupChat, room__name=room)
        return query
     
    def retrieve(self, request, room, **kwargs):
        instance = self.get_object(room)
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        

#Join Group
class GroupJoinAPIView(APIView):
    """
    Join a group with the post request , 
    delete request will remove user from the group specified
    and get query should list all current group of user 
    """
    permission_classes = [IsAuthenticated]
#    serializer_class = JoinGroupSerializer

    def get_object(self,room):
        try:
            queryset = GroupChat.objects.get(room__name = room)
            return queryset
        except GroupChat.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippet = request.user.groupchat_set.all()
        serializer = GroupSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            room = request.data['room']
        except :
            raise Http404
        ola = self.get_object(room)
        if request.user.groupchat_set.filter(room__name=room):
            return Response('already regis')
        
        serializer = JoinGroupSerializer(data={'room':room,
        'user' : request.META.get('HTTP_AUTHORIZATION') 
        })

        ola.citizens.add(request.user)
        ola.save()
        #scale later

        redis_client.sadd(f"user:{request.user.id}:rooms", f"{ola.id}")
        redis_client.sadd(f"room:{ola.id}:users", f"{request.user.name}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #leave chat 
    def delete(self, request, room, format=None):
        snippet = self.get_object(room)
        #check if in room
        if request.user.groupchat_set.filter(room__name=room):
            request.user.groupchat_set.remove(room)
            redis_client.srem(f"user:{request.user.id}:rooms", f"{snippet.id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return 'not in room'
    

#add other admins
class AddAdminView(APIView):
    #check if user is admin
    serializer_class = JoinGroupSerializer
    permission_classes = [GroupOwners]
    def get_object(self,room):
        try:
            queryset = Room.objects.get(name = room)
            self.check_object_permissions(self.request, queryset)
            return queryset
        except GroupChat.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        try:
            room = request.data['room']
            admin = request.data['user']
        except :
            raise Http404
        ola = self.get_object(room)
        #username
        user =User.objects.get(username=admin)
        #if user in group
        serializer = JoinGroupSerializer(data={'room':room,
        'user' : admin 
        })
        if user.groupchat_set.filter(room__name=room):
            ola.admin.add(user)
            ola.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Http404
        
class CheckUSer(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def saveprivate(message):
    userid = message.id

    


def SaveGroupMessage(message):
    room = message.roomId
    message = message.message
    date = message.date
    room  =  Room.objects.get(pk=room)
    p, created = RoomMessage.get_or_create(
        Room = room,
        date =date,
        message= message
    )




    
#delete group
class DeleteGroup(APIView):
    '''
    delete group created
    
    '''
    permission_classes = [GroupCreator]
    def get_object(self,room):
        try:
            queryset = Room.objects.get(name = room)
            self.check_object_permissions(self.request, queryset)
            return queryset
        except GroupChat.DoesNotExist:
            raise Http404
    def post(self, request):
        room = request.data['room']
        ola = self.get_object(room)
        redis_client.delete(f"room:{ola.id}:name")
        redis_client.srem(f"user:{request.user.id}:rooms", f"{ola.id}")
        ola.delete()
        
        return 'deleted'
# from rest_framework_gis.filters import DistanceToPointFilter

# class LocationList(ListAPIView):

#     queryset = MapPoint.objects.all()
#     serializer_class = LocationSerializer
#     distance_filter_field = 'geometry'
#     filter_backends = (DistanceToPointFilter,)

#save discussion
    #receives from redis pub and save message



# class GroupJoinAPIView(CreateAPIView):
#    # queryset = GroupChat.objects.all()
#     serializer_class = JoinGroupSerializer

#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = GroupChat.objects.all()
#         room = self.request.data.get('room')
#         if room is not None:
#             queryset = queryset.filter(room__name=room).first()

#         return queryset,room

#     def create(self, request, *args, **kwargs):
#         #check if user is already in group
#         ola,room = self.get_queryset()
#         if not hasattr(ola, 'citizens'):
#             return Response('not ac')
#         elif request.user.groupchat_set.filter(room__name=room):
#             return Response('already regis')
#         ola.citizens.add(request.user)
#         ola.save()
#         print('ok')

#         RedisPub('joingroup',serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def RedisPub(channel_name,SerializerData):
    #push to redis 
     redis_client.subscribe(channel_name, SerializerData)

#receive message check if private and store in message, then check if public and store in public
