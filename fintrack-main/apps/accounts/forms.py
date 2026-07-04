from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            'class': 'form-control',
            'id': 'full_name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'name@company.com',
            'class': 'form-control',
            'id': 'email'
        })
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'form-control',
            'id': 'username'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and custom IDs for JS checks to passwords
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control',
            'id': 'password1'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control',
            'id': 'password2'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'name@company.com or username',
            'class': 'form-control',
            'id': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control',
            'id': 'password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        })
    )


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'name@company.com',
            'class': 'form-control',
            'id': 'email'
        })
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': '••••••••'
            })
