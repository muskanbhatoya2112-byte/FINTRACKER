from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows logging in using either
    the username or the email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            # Check if username is an email
            if '@' in username:
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
