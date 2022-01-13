from django.http.response import Http404
from django.urls.base import clear_script_prefix
from django_filters.rest_framework.backends import DjangoFilterBackend
from authentication.permissions import AuthorOrReadOnly
from novel.models import Audio, Genre,Profile, Novel, Poems, Weekly, Chapters, UserBook
from rest_framework import generics, serializers, viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from .serializers import AudioSerializer, ChapterSerializer,UserNovelSerializer, AuthorSerializer, GenreSerializer, NovelSerializer, PoemSerializer, UserSerializer,  WeeklySerializer
from django.contrib.auth import get_user_model
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from api.filters import NovelFilter
User = get_user_model()


class NovelRealease(generics.ListAPIView):
    """
    Every Novel ordered accoring to date uploaded
    """
    queryset = Novel.objects.all().order_by('-date_uploaded')
    serializer_class = NovelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class NovelSearchView(generics.ListAPIView):
    """
    Displays all novels with just 'get request' , filters the searches with ?search query ;
    e.g
     /novel-search?genre=&author= 
    
    will return all novel objects relating to ola
    
    
    """
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    permission_classes =[permissions.AllowAny,]
    filter_backends = [DjangoFilterBackend]
    filter_class = NovelFilter
    #search_fields = ['title', 'author__authorName', 'genre__name', 'books__title']
 

class PoemsSearchView(generics.ListAPIView):
    """
    Displays all poems with just 'get request' , filters the searches with ?search query ;
    e.g
     /poem-search?search=ola 
    
    will return all poems objects relating to ola
    
    
    """
    queryset = Poems.objects.all()
    serializer_class = PoemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'authorName', 'genre', 'chapter_title']

class AudiosListView(generics.ListAPIView):
    """
    Search Audios , fields are title , author genre, chapters
    """
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'authorName', 'genre', 'chapter_title']


class PoemsListView(generics.ListAPIView):
    """
    searches through the poems available on the website
    
    """
    queryset = Poems.objects.all()
    serializer_class = PoemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'authorName', 'genre', 'chapter_title']


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def home(request):
    '''
    Displays Genres , Weely Novels , Audios , Special Features, Authors .....

    Sends back all the genres listed also .

    Designed For The Hopepage 
    
    '''
    weekly = Weekly.objects.all()
    week_serializer = WeeklySerializer(weekly, many=True)
    genres  =  Genre.objects.all()
    genre_serializer = GenreSerializer(genres, many=True)
    # add blog
    return Response({'genres':genre_serializer.data, 'weekly':week_serializer.data})



class RecentReadViewSet(APIView):
    """
    list all recently viewed novels chapters of logged in user, 

    """
    
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        recent = request.user.recently_viewed_chapters.all()
        serializer = ChapterSerializer(recent, many=True)
        return Response(serializer.data)


class ReadChapter(APIView):
    """
    Returns the Chapter of the Novel 
    read/<book>/<chapter>

    if Chapter not specified , it returns the last chapter read by the user for that particular book, 
    else if its the user's first time of reading the book it returns the first chapter of the book
    
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self, book):
        try:
            novel = Novel.objects.get(slug=book)
            ola , created = UserBook.objects.get_or_create(user=self.request.user,book=novel)
            return novel
        except Novel.DoesNotExist:
            raise Http404
    def get(self, request, book, pk=None,format=None ):
        #change bookstatus
        
        book = self.get_object(book)
        
        user =request.user.recently_viewed_chapters
        if pk:
            try:
                chapter =book.books.get(pk=pk)
                
            except ObjectDoesNotExist:
                raise Http404
            
            try :
                #if a chapter of the book exist , just update
                novel = user.get(novel=book)
                user.remove(novel)
                user.add(chapter)
            except ObjectDoesNotExist:
                user.add(chapter)
                
            request.user.save()
 
            serializer = ChapterSerializer(chapter)
            return Response(serializer.data)
        # get the recently read chapter for that novel by the user
        try:
            chapter = user.get(novel=book)
        except ObjectDoesNotExist:
            # send chapter 1
            # check if chapter 1 exist
            
            chapter = book.books
            chapter = chapter.first()
            if not chapter.exists():
                raise Http404
            user.add(chapter)
            request.user.save()
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)

        # if no pk return recent chapter in novel

class BookStatusUpdate(APIView):

    """
    Returns completed Novels and still reading (that is unread novels)...
    also uses the put request to update state of the novel , upon completion users can put a request to change the state of the novel 
    they have finished reading
    """
    queryset = UserBook.objects.all()
    serializer_class = UserNovelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):    
        book = UserBook.objects.filter(user=self.request.user)
       # print(self.request.user)
        if not list(book):
            raise Http404("No MyModel matches the given query.")

        return book


    def get(self, request, book=None):

        instance = self.get_object()
        # print(instance)
        if book:
            books = instance.filter(state='u')
            serializer = UserNovelSerializer(books, many=True)
            return Response(serializer.data)

        books = instance.filter(state='r')
        serializer = UserNovelSerializer(books, many=True)
        return Response(serializer.data)
        

    def put(self, request, book, format=None):
        try:
            snippet = self.get_object().filter(book__slug=book).get()
        except ObjectDoesNotExist:
            raise Http404
        
        data = {'state': request.data.get('state')}
        serializer = UserNovelSerializer(snippet, data=data, partial=True)
        if serializer.is_valid(raise_exception=True) and snippet:
            serializer.update(serializer, data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class AuthorView(APIView):
    """"
    Author Bio 
    Return Number of books , best selling books , genres, new , most popular, number of read,
    """
    permission_classes = [permissions.AllowAny]
    def get_object(self, pk):
        try:
            author = Profile.objects.get(pk=pk)
        except :
            raise Http404
        return author


    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

        

class CurrentUser(APIView):
    """
    Sends Current Logged in User Details User's Detail
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# Create Books , only authors can create books 
class CreateBook(APIView):
    """
    Allows Authors to create their novels 
    """
    permission_classes = (permissions.IsAuthenticated,AuthorOrReadOnly)
    serializer_class = NovelSerializer
    def post(self, request):
        serializer = NovelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


