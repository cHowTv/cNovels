from drf_yasg.views import get_schema_view
from django.urls import path
from rest_framework import permissions
from drf_yasg import openapi
from .views import AddAdminView, GroupCreateAPIView, GroupJoinAPIView, GroupMembersList, CheckUSer


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


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
    # ...
    path('create', GroupCreateAPIView.as_view()),
    path('join', GroupJoinAPIView.as_view()),
    path('member-list/<str:room>',GroupMembersList.as_view()),
    path('add-admin/',AddAdminView.as_view()) ,
    path('intrest',CheckUSer.as_view())
    

]