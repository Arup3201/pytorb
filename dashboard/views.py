from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import services

@login_required
def dashboard(request):
    user = request.user

    my_projects = services.get_my_projects(user=user)
    task_summary = services.get_task_summary(user=user)
    recent_notifications = services.get_recent_notifications(user=user)

    context = {
        "active_page": 'dashboard',
        "total_projects": my_projects.count(),
        "total_tasks": task_summary['total_tasks'],
        "in_progress_tasks": task_summary['in_progress_tasks'],
        "completed_tasks": task_summary['completed_tasks'],
        "recent_tasks": task_summary['my_tasks'],
        "recent_projects": my_projects[:4],
        "recent_notifications": recent_notifications,
    }

    return render(request, "dashboard.html", context)
