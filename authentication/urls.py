from django.urls import path
from .views import register , activateAccount , login_view, logout_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', register, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activateAccount, name='activate'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='novel/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='novel/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='novel/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='novel/password_reset_done.html'), name='password_reset_complete'),
   
]