from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import services, forms
from tasks.forms import TaskForm
from tasks import services as task_services

@login_required
def list(request):
    if request.method == "GET":    
        search = request.GET.get('search', "")
        sort = request.GET.get('sort', 'updated')
        page_number = request.GET.get('page', 1)
        page_obj = services.get_projects_list(user=request.user, search=search, sort=sort, page_number=page_number)
        form = forms.ProjectForm()
        return render(request, 'list.html', {'active_page': 'projects', 'page_obj': page_obj, 'search': search, 'sort': sort, 'form': form})
    
    elif request.method == "POST":
        form = forms.ProjectForm(request.POST)

        if not form.is_valid():
            messages.add_message(request, messages.ERROR, "\n".join([str(error) for error in form.non_field_errors()]))
        else:
            title = form.data["title"]
            description = form.data["description"]
            topics = form.data["topics"]
            services.create_project(title=title, description=description, topics=topics, user=request.user)
            messages.add_message(request, messages.SUCCESS, "Project has been created successfully.")

    else:
        messages.add_message(request, messages.ERROR, "Method not allowed on this URL")

    return HttpResponseRedirect(reverse('projects:list'))

@login_required
def index(request, pk):
    if request.method == 'GET':
        project = services.get_project(user=request.user, project_id=pk)
        if not project:
            raise Http404("Project does not exist")
        
        form = forms.ProjectForm(instance=project)
        task_form = TaskForm()

        section = request.GET.get('section', 'tasks')
        search = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        if section == 'tasks':
            sort = request.GET.get('sort', 'updated')
            page_obj = task_services.list_tasks(project_id=pk, search=search, sort=sort, page_number=page_number)
        elif section == 'members':
            sort = request.GET.get('sort', 'joined')
            page_obj = services.list_members(project_id=pk, search=search, sort=sort, page_number=page_number)
        else:
            sort = ''
            page_obj = []

        return render(request, 'index.html', {'active_page': 'projects', 'project_section': section, 'project': project, 'form': form, 'task_form': task_form, 'page_obj': page_obj, 'search': search, 'sort': sort, 'page': page_number})
    else:
        messages.add_message(request, messages.SUCCESS, "URL method is not allowed!")
    
    return redirect('projects:index', pk=pk)

@login_required
def edit(request, pk):
    form = forms.ProjectForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR, "\n".join([str(error) for error in form.non_field_errors()]))
    else:
        title = form.data['title']
        description = form.data['description']
        topics = form.data['topics']
        services.edit_project(pk=pk, title=title, description=description, topics=topics)
        messages.add_message(request, messages.SUCCESS, "Project has been updated successfully.")

    return redirect('projects:index', pk=pk)

@login_required
def get_projects_for_user(request):
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'created')
    page_number = request.GET.get('page', 1)
    page_obj = services.get_projects_for_user(user=request.user, search=search, sort=sort, page_number=page_number)

    return render(request, 'explore.html', {'active_page': 'explore', 'page_obj': page_obj, 'search': search, 'sort': sort, 'page': page_number})

@login_required
def join_requests(request, pk):
    if request.method == 'POST':
        pass

    return redirect('projects:index', pk=pk)