from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordChangeView as DjangoPasswordChangeView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, CustomPasswordChangeForm

class RegisterView(CreateView):
    """
    Handles user registration using custom RegisterForm.
    Redirects to Login with success message.
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please sign in.")
        return response


class LoginView(DjangoLoginView):
    """
    Handles user login using custom LoginForm.
    Manages remember-me session duration (30 days vs browser session).
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        response = super().form_valid(form)
        
        if remember_me:
            # Set session to expire in 30 days (in seconds)
            self.request.session.set_expiry(2592000)
        else:
            # Expiry on browser close
            self.request.session.set_expiry(0)
            
        messages.success(self.request, f"Welcome back, {self.request.user.full_name or self.request.user.username}!")
        return response


class LogoutView(DjangoLogoutView):
    """
    Handles user logout and redirects back to the public landing page.
    """
    next_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, DjangoPasswordChangeView):
    """
    Handles secure password changes for logged-in users.
    Protected using LoginRequiredMixin.
    """
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password was changed successfully!")
        return response


class ForgotPasswordView(DjangoPasswordResetView):
    """
    Triggers password reset email delivery.
    """
    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot_password.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    """
    Displays confirmation that a password reset link was sent.
    """
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    """
    Displays form to enter a new password after clicking the reset link.
    """
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    """
    Displays password reset completion message.
    """
    template_name = 'accounts/password_reset_complete.html'
