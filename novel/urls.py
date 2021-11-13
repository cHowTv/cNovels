from rest_framework.schemas import get_schema_view
from django.urls import path
from .views import AddAdminView, GroupCreateAPIView, GroupJoinAPIView, GroupMembersList, CheckUSer

urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('docs/', get_schema_view(
        title="cNovels",
        description="API for cNovels",
        version="1.0.0"
    ), name='docs-schema'),
    # ...
    path('create', GroupCreateAPIView.as_view()),
    path('join', GroupJoinAPIView.as_view()),
    path('member-list/<str:room>',GroupMembersList.as_view()),
    path('add-admin/',AddAdminView.as_view()) ,
    path('intrest',CheckUSer.as_view())
    

]