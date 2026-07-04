from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, help_text="User's full name from registration.")

    def __str__(self):
        return self.full_name or self.username
