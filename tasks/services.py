from django.core.paginator import Paginator
from django.db import transaction
from . import models
from projects.models import Project, Member

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

def get_assignees(*, task: models.Task):
    return task.assignee_set.values_list('user_id', flat=True)

def get_project_members(*, project_id: str):
    return Member.objects.filter(project_id=project_id)

def update_task(*, task_id: str, title: str|None = None, description: str|None = None, status: str|None = None):
    task = models.Task.objects.get(id=task_id)
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    task.save()

def update_assignees(*, task_id: str, assignees: list[str]):
    task = models.Task.objects.get(id=task_id)

    with transaction.atomic():
        existing_task_assignees = task.assignee_set.values_list('user_id', flat=True)
        for assignee in existing_task_assignees:
            if assignee not in assignees:
                models.Assignee.objects.filter(task_id=task_id, user_id=assignee).delete()
        for assignee in assignees:
            if assignee not in existing_task_assignees:
                models.Assignee.objects.create(task_id=task_id, user_id=assignee)
    
def create_comment(*, task_id: str, author: str, comment: str):
    models.Comment.objects.create(task_id=task_id, user_id=author, content=comment)

def get_permissions_on_task(*, project_id: str, task_id: str, user: models.User):
    project = Project.objects.get(id=project_id)
    if project.owner.pk == user.pk:
        return ["task:edit", "task:assign"]

    assignee = models.Assignee.objects.filter(task_id=task_id, user_id=user.pk)
    if assignee:
        return ["task:edit"]

    return []