from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks import forms, services

@login_required
def create_task(request, pk):
    form = forms.TaskForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR, "\n".join([str(error) for error in form.non_field_errors()]))
    else:
        title = form.data.get('title', '')
        description = form.data.get('description', '')
        status = form.data.get('status', '')
        services.create_task(project_id=pk, title=title, description=description, status=status)
        messages.add_message(request, messages.SUCCESS, "A new task has been added successfully.")

    return redirect('projects:index', pk=pk)

@login_required
def index(request, pk, task_id):
    task = services.get_task(task_id=task_id)
    if not task:
        raise Http404("Task not found")

    assignees = services.get_assignees(task=task)
    members = services.get_project_members(project_id=pk)
    permissions = services.get_permissions_on_task(project_id=pk, 
                                                   task_id=task_id, 
                                                   user=request.user)
    can_assign = False
    if "task:assign" in permissions:
        can_assign = True
    can_edit = False
    if "task:edit" in permissions:
        can_edit = True
    return render(request, 'task.html', {'active_page': 'projects', 'task': task, 'project_members': members, 'assignees': assignees, 'can_edit': can_edit, 'can_assign': can_assign})

@login_required
def update(request, pk, task_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        services.update_task(task_id=task_id, title=title, description=description, status=status)
        messages.add_message(request, messages.SUCCESS, "Task has been updated successfully.")

    return redirect('projects:task_index', pk=pk, task_id=task_id)

@login_required
def update_assignees(request, pk, task_id):
    if request.method == 'POST':
        assignees = request.POST.getlist("assignees")
        services.update_assignees(task_id=task_id, assignees=assignees)
        messages.add_message(request, messages.SUCCESS, "Task assignees updated.")
    return redirect('projects:task_index', pk=pk, task_id=task_id)

@login_required
def create_comment(request, pk, task_id):
    if request.method == 'POST':
        comment = request.POST.get('content')
        messages.add_message(request, messages.SUCCESS, "Comment has been added.")
        services.create_comment(task_id=task_id, author=request.user.id, comment=comment)

    return redirect('projects:task_index', pk=pk, task_id=task_id)
