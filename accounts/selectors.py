from django.core.files.storage import default_storage
from . import models

def get_user_profile_data(*, user: models.User):
    if user.avatar_key:
        avatar_url = default_storage.url(user.avatar_key)
    else:
        avatar_url = None

    return {
        'avatar_url': avatar_url,
        'display_name': f"{user.first_name} {user.last_name}", 
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email, 
        'username': user.username, 
        'skills': user.skills, 
        'total_projects': 12,
        'total_tasks_completed': 87,
        'task_completion_rate': f"{87/100:.2f}"
    }