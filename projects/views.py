from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import services, forms

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    if request.method == "GET":    
        search = request.GET.get('search', "")
        sort = request.GET.get('sort', 'updated')
        page_number = request.GET.get('page', 1)
        page_obj = services.get_projects_list(search=search, sort=sort, page_number=page_number)
        form = forms.CreateProjectForm()
        return render(request, 'index.html', {'active_page': 'projects', 'page_obj': page_obj, 'search': search, 'sort': sort, 'form': form})
    
    elif request.method == "POST":
        form = forms.CreateProjectForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, "\n".join([str(error) for error in form.non_field_errors()]))
        else:
            title = form.data["title"]
            description = form.data["description"]
            topics = form.data["topics"]
            services.create_project(title=title, description=description, topics=topics, user=request.user)
            messages.add_message(request, messages.SUCCESS, "Project has been created successfully.")
            return HttpResponseRedirect(reverse('projects:index'))
    else:
        messages.add_message(request, messages.ERROR, "Method not allowed on this URL")
        return HttpResponseRedirect(reverse('projects:index'))
