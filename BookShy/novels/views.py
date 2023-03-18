from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter

from .serializers import NovelSerializer, ChapterSerializer
from .models import NovelModel

from django_filters.rest_framework.backends import DjangoFilterBackend

# Create your views here.
class NovelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        weekly_featured = request.query_params.get('weekly_featured', None)

        special_featured = request.query_params.get('special_featured', None)

        if weekly_featured is not None and weekly_featured.lower() == 'true':
            novels = NovelModel.objects.filter(publish=True, weekly_featured=True)

        elif special_featured is not None and special_featured.lower() == 'true':
            novels = NovelModel.objects.filter(publish=True, special_featured=True)
        
        else:
            novels = NovelModel.objects.filter(publish=True)

        serializers = NovelSerializer(novels , many=True)
        return Response({'status': 'success',
            'data': serializers.data}, status=status.HTTP_200_OK
        )
        


class RecentReadViewSet(APIView):
    """
    list all recently viewed novels chapters of logged in user, 

    """
    
    permission_classes = [IsAuthenticated]
    my_tags = ['Book', 'Home']

    def get(self, request):
        recent = request.user.recently_viewed_chapters.all().select_related('book')
        serializer = ChapterSerializer(recent, many=True)

        return Response({'status': 'success',
            'data': serializer.data}, status=status.HTTP_200_OK
        )
    

class NovelSearchView(APIView):
    """
    Displays all novels with just 'get request' , filters the searches with ?search query ;
    e.g
     /novel/search=mkmkmk?genre=&author= 
    
    will return all novel objects relating to ola
    
    """
    queryset = NovelModel.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genre']
    search_fields = ['title']
