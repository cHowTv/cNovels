from django.urls import path, include
from .views import GoogleLogin,VerifyAccount,VerifyPageView, MyTokenObtainPairView, ProfileViewset, RegisterView, UserInterestView,  logout_user
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path("interest", UserInterestView.as_view(), name='interest'),
    path("verified-email-page", VerifyPageView.as_view(), name='verified-email-page'),
    path('logout/', logout_user.as_view(), name='logout'),
    path('register/' , RegisterView.as_view(), name = 'auth_register'),
    path('reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('author_profile/', ProfileViewset.as_view()),
    path('activate/<int:uidb64>/<token>/',VerifyAccount.as_view(), name='activate' )
]