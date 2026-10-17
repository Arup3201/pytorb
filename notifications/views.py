from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import services

@login_required
def list(request):
    page_number = request.GET.get('page', 1)
    page_obj = services.list_notifications(user=request.user, page_number=page_number)
    return render(
        request,
        "notification.html",
        {
            'active_page': 'notifications',
            'page_obj': page_obj,
            'notifications': page_obj,
            'page': page_number,
        }
    )