
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from .views import AddAdminView, GroupCreateAPIView, GroupJoinAPIView, GroupMembersList




urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
   # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # ...
    path('create', GroupCreateAPIView.as_view()),
    path('join', GroupJoinAPIView.as_view()),
    path('member-list/<str:room>',GroupMembersList.as_view()),
    path('add-admin/',AddAdminView.as_view()),
    
    

]