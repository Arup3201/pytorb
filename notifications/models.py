from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class Notification(models.Model):
    class EventType(models.TextChoices):
        PROJECT_UPDATED = "project.update", _("Project Updated")
        JOIN_REQUEST_ADDED = "project.join_request", _("Join Request Added To Project")
        JOIN_REQUEST_RESPONDED = "project.join_response", _("Response To Join Request")
        TASK_ADDED = "task.add", _("Task Added")
        TASK_UPDATED = "task.update", _("Task Updated")
        TASK_ASSIGNEE_ADDED = "task.assignee.add", _("Task Assignee Added")
        TASK_ASSIGNEE_REMOVED = "task.assignee.remove", _("Task Assignee Removed")
        TASK_COMMENT_ADDED = "task.comment.add", _("Task Comment Added")

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    actor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name="notifications_sent"
    )
    event_type = models.CharField(max_length=100, choices=EventType)
    payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["recipient", "-created_at"],
            ),
        ]

    def __str__(self):
        return f"{self.event_type} -> {self.recipient}"