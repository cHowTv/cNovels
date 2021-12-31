from django import urls
from django.db import router
from django.urls import include, path
from rest_framework import routers
from .api import BookStatusUpdate, NovelSearchView, CurrentUser,PoemsSearchView, RecentReadViewSet, CreateBook, home, ReadChapter, AuthorView





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('people', home, name='people'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('novel-search/', NovelSearchView.as_view()),
    path('poem-search/', PoemsSearchView.as_view()),
    path('recent_novels/', RecentReadViewSet.as_view()),
    path('', home),
    path('read/<slug:book>',ReadChapter.as_view()),
    path('read/<slug:book>/<int:pk>',ReadChapter.as_view()),
    path('book_status',BookStatusUpdate.as_view()),
    path('book_status/<slug:book>',BookStatusUpdate.as_view()),
    path('author/<int:pk>', AuthorView.as_view()),
    path('current_user',CurrentUser.as_view()),
    path('upload_book', CreateBook.as_view())
]