from django.urls import path
from .views import register , activateAccount

urlpatterns = [
    path('signup/', register, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activateAccount, name='activate'),
]