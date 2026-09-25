from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar_key = models.TextField()
    skills = models.CharField(max_length=255)