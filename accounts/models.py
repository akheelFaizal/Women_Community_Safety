from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_moderator = models.BooleanField(default=False, help_text="Designates whether this user can moderate reports.")
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
