from django import urls
from django.db import router
from django.urls import include, path
from rest_framework import routers
from .api import NovelSearchView, PoemsSearchView, RecentReadViewSet, home





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('people', home, name='people'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('novel-search/', NovelSearchView.as_view()),
    path('poem-search/', PoemsSearchView.as_view()),
    path('recent_novels/', RecentReadViewSet.as_view()),
    path('', home),
    path('recent_novels/<str:pk>', RecentReadViewSet.as_view())
]