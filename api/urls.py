from django import urls
from django.db import router
from django.urls import include, path
from rest_framework import routers
from .api import NovelSearchView, RecentReadViewSet





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('people', home, name='people'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('questions/', NovelSearchView.as_view()),
    path('recent_novels/', RecentReadViewSet.as_view()),
    path('recent_novels/<str:pk>', RecentReadViewSet.as_view())
]