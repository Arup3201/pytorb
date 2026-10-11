from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, SoftDeleteModel
from projects.models import Project
from accounts.models import User

class Task(BaseModel):
    class TaskStatus(models.TextChoices):
        TODO = "TD", _("To Do")
        INPROGRESS = "IP", _("In Progress")
        DONE = "DN", _("Done")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=TaskStatus, default=TaskStatus.TODO)

class Assignee(BaseModel, SoftDeleteModel):
    class Meta(BaseModel.Meta, SoftDeleteModel.Meta):
        pass

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(BaseModel):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='comment text')