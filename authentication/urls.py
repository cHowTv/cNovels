from django.urls import path
from .views import GoogleLogin, MyTokenObtainPairView, ProfileViewset, RegisterView, UserIntrestView,  logout_user
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path("interest", UserInterestView.as_view()),

    path('logout/', logout_user, name='logout'),
    path('register/' , RegisterView.as_view(), name = 'auth_register'),
#    path('activate/<uidb64>/<token>/', activateAccount, name='activate'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='novel/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='novel/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='novel/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='novel/password_reset_done.html'), name='password_reset_complete'),
    path('author-profile/', ProfileViewset.as_view())
]