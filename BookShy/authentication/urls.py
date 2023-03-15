from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import MyTokenObtainPairView, UserRegistration, VerifyAccount, UserInterestView


urlpatterns = [
    path('register/', UserRegistration.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uidb64>/<str:token>/', VerifyAccount.as_view(), name='activate'),
    path('interest/', UserInterestView.as_view(), name='interest'),
    
]