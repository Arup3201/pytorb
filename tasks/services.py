from django.core.paginator import Paginator
from . import models
from projects.models import Project

def create_task(*, project_id: str, title: str, description: str, status: str):
    project = Project.objects.get(id=project_id)
    task = models.Task(title=title, description=description, status=status, project=project)
    task.save()

def list_tasks(*, project_id: str, search: str = "", sort: str = 'updated', page_number: int = 1):
    tasks = models.Task.objects.all()
    tasks = tasks.filter(project_id=project_id)
    if search:
        tasks = tasks.filter(title__contains = search)

    if sort == 'title':
        tasks = tasks.order_by('title')
    elif sort == 'created':
        tasks = tasks.order_by('-created_at')
    elif not sort or sort == 'updated':
        tasks = tasks.order_by('-updated_at')

    paginator = Paginator(tasks, 5)
    page_obj = paginator.get_page(page_number)

    return page_obj

def get_task(*, task_id: str):
    try:
        task = models.Task.objects.get(id=task_id)
    except models.Task.DoesNotExist:
        return None
    else:
        return task