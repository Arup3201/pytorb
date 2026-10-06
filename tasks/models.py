from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from projects.models import Project

class Task(BaseModel):
    class TaskStatus(models.TextChoices):
        TODO = "TD", _("To Do")
        INPROGRESS = "IP", _("In Progress")
        DONE = "DN", _("Done")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=TaskStatus, default=TaskStatus.TODO)
