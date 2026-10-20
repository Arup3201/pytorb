from django.core.files.storage import default_storage
from . import models
from projects.models import Project
from tasks.models import Task

def get_user_profile_data(*, user: models.User):
    if user.avatar_key:
        avatar_url = default_storage.url(user.avatar_key)
    else:
        avatar_url = None

    total_projects = Project.objects.filter(member__user=user).count()
    tasks = Task.objects.filter(assignee__user=user)
    total_tasks = tasks.distinct().count()
    total_completed_tasks = tasks.filter(status=Task.TaskStatus.DONE).distinct().count()

    return {
        'avatar_url': avatar_url,
        'display_name': f"{user.first_name} {user.last_name}", 
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email, 
        'username': user.username, 
        'skills': user.skills, 
        'total_projects': total_projects,
        'total_tasks_completed': total_completed_tasks,
        'task_completion_rate': f"{round(total_completed_tasks/total_tasks, 2) if total_tasks > 0 else 'N/A'}"
    }