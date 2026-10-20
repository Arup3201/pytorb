from django.db.models import Count
from projects.models import Project
from tasks.models import Task
from accounts.models import User
from notifications.models import Notification

def get_my_projects(*, user: User):
    return (
        Project.objects
        .filter(member__user=user)
        .annotate(
            task_count=Count("task", distinct=True),
            member_count=Count("member", distinct=True),
        )
        .order_by("-updated_at")
    )

def get_task_summary(*, user: User):
    my_tasks = Task.objects.filter(assignee__user=user)
    total_tasks = my_tasks.distinct().count()
    in_progress_tasks = my_tasks.filter(status=Task.TaskStatus.INPROGRESS).distinct().count()
    completed_tasks = my_tasks.filter(status=Task.TaskStatus.DONE).distinct().count()
    return {
        "total_tasks": total_tasks, 
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "my_tasks": my_tasks
            .exclude(status=Task.TaskStatus.DONE)
            .select_related("project")
            .distinct()
            .order_by("-updated_at")[:5]
    }

def get_recent_notifications(*, user: User):
    return (
        Notification.objects
            .filter(recipient=user)
            .order_by("-created_at")[:5]
    )
