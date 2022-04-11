
from .documentation import schema_view
from django.urls import path
from .views import AddAdminView, GroupCreateAPIView, GroupJoinAPIView, GroupMembersList




urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
   # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'
         ),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'
         ),
    # ...
    path('create', GroupCreateAPIView.as_view()),
    path('join', GroupJoinAPIView.as_view()),
    path('member-list/<str:room>',GroupMembersList.as_view()),
    path('add-admin/',AddAdminView.as_view()),
    
    

]