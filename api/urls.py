from django.urls import path
from .views import AddAdminView, GroupCreateAPIView, GroupJoinAPIView, GroupMembersList





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('create', GroupCreateAPIView.as_view()),
    path('join', GroupJoinAPIView.as_view()),
    path('member-list/<str:room>',GroupMembersList.as_view()),
    path('add-admin/',AddAdminView.as_view()),
    #path('people', home, name='people'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)