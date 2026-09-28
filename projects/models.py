from django.db import models
from accounts.models import User

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
