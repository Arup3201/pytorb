from django.core.paginator import Paginator
from accounts.models import User
from . import models

def get_projects_list(*, search: str = "", sort: str = "updated", page_number: int = 1):
    projects = models.Project.objects.all()
    if search:
        projects = projects.filter(title__contains = search)

    if not sort:
        sort = "updated"
    if sort == 'title':
        projects = projects.order_by('title')
    elif sort == 'created':
        projects = projects.order_by('-created_at')
    elif sort == 'updated':
        projects = projects.order_by('-updated_at')

    paginator = Paginator(projects, 3)
    page_obj = paginator.get_page(page_number) 

    return page_obj

def create_project(*, title: str, description: str, topics: str, user: User):
    models.Project.objects.create(title=title, description=description, topics=topics, owner=user)

def edit_project(*, pk: str, title: str, description: str, topics: str):
    project = models.Project.objects.get(pk=pk)
    project.title = title
    project.description = description
    project.topics = topics
    project.save()
