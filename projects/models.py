from django.db import models
from accounts.models import User
from core.models import BaseModel

class Project(BaseModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.CharField(max_length=255)
