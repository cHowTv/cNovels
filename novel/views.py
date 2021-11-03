#join group api

#Create Group
from os import name
from django.db.models import query
from django.http.response import Http404
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import AuthorOrReadOnly, GroupOwners
from novel.models import GroupChat, Room
from rest_framework.response import Response
from novel.serializers import GroupMessageSerializer, JoinGroupSerializer, RoomSerializer
import redis
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Connect to our Redis instance
redis_instance = redis.StrictRedis(host='172.26.255.129', 
  port= 6379,
                              #    port=settings.REDIS_PORT,
                               db=0)
#create group 
class GroupCreateAPIView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AuthorOrReadOnly]

    def perform_create(self, serializer):
        
        serializer.save(creator= self.request.user, admins = 
        [self.request.user])
      


#Members list Group
class GroupMembersList(RetrieveAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupMessageSerializer
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
    Join a group 
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
        serializer = GroupMessageSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            room = request.data['room']
        except :
            raise Http404
        ola = self.get_object(room)
        print(request.META.get('access') )
        if request.user.groupchat_set.filter(room__name=room):
            return Response('already regis')
        
        serializer = JoinGroupSerializer(data={'room':room,
        'user_token' : request.META.get('HTTP_AUTHORIZATION') 
        })

        ola.citizens.add(request.user)
        ola.save()
        print(serializer)
        RedisPub('joingroup',serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    






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
     redis_instance.publish(channel_name, SerializerData)

