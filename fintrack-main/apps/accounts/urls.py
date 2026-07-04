from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Password Reset flow
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
