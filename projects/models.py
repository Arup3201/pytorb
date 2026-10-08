from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from core.models import BaseModel

class Project(BaseModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.CharField(max_length=255)

class MemberType(models.TextChoices):
    OWNER = "OWN", _("Owner")
    MEMBER = "MEM", _("Member")

class Member(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member_type = models.CharField(max_length=6, choices=MemberType, default=MemberType.MEMBER)
