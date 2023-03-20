from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)


from django.urls import path
from .views import MyTokenObtainPairView, UserInterestView, RegisterView, ResendMail



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('interest/', UserInterestView.as_view()),
    path('login/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-email', ResendMail.as_view())
 
    
]