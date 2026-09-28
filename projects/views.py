from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from . import models

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    
    user = request.user
    if user.avatar_key:
        avatar_url = default_storage.url(user.avatar_key)
    else:
        avatar_url = None
    profile_info = {
        'avatar_url': avatar_url,
        'display_name': f"{user.first_name} {user.last_name}", 
        'username': user.username, 
    }

    projects = models.Project.objects.all()
    paginator = Paginator(projects, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)    
    return render(request, 'index.html', {'profile': profile_info, 'page_obj': page_obj})
