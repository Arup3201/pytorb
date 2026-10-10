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
    return render(request, 'task.html', {'active_page': 'projects', 'task': task})