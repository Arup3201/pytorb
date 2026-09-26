import traceback
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.files.storage import default_storage
from . import models

def register_account(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, "Confirm Password does not match the Password!")
        else:
            try:
                user = models.User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.add_message(request, messages.SUCCESS, "You have been successfully registerd to Task Orbit!")
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Email/Username already exist. Please try to login instead...")
            except Exception as e:
                traceback.print_exception(e)
                messages.add_message(request, messages.ERROR, "Something went wrong. Please try again.")
    return render(request, "register.html")

def login_account(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("accounts:profile"))
        else:
            messages.add_message(request, messages.ERROR, "Username/Password is not correct!")
    elif request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("accounts:profile"))

    return render(request, "login.html")

def profile(request):
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
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email, 
        'username': user.username, 
        'skills': user.skills, 
        'total_projects': 12,
        'total_tasks_completed': 87,
        'task_completion_rate': f"{87/100:.2f}"
    }
    return render(request, 'profile.html', {'profile': profile_info})

def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

def edit_account(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Request method POST is not allowed!")
        return HttpResponseRedirect(reverse('accounts:profile'))

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    skills = request.POST.get("skills")

    user = models.User.objects.get(id=request.user.id)
    user.first_name = first_name
    user.last_name = last_name
    user.skills = skills
    try:
        user.save()
    except:
        messages.add_message(request, messages.ERROR, "Something went wrong. Please try again...")
        return HttpResponseRedirect(reverse('accounts:profile'))

    messages.add_message(request, messages.SUCCESS, "User profile data has been updated!")
    return HttpResponseRedirect(reverse('accounts:profile'))

def edit_avatar(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Only POST method not allowed for this URL")
        return HttpResponseRedirect(reverse('accounts:profile'))
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))

    file = request.FILES['avatar']
    file_key = f"users/{request.user.id}/avatars/{file.name}"
    try:
        default_storage.save(file_key, file)
    except Exception as e:
        traceback.print_exception(e)
        messages.add_message(request, messages.ERROR, "Failed to edit the image! Please try again.")
        return HttpResponseRedirect(reverse('accounts:profile'))

    try:
        user = models.User.objects.get(id=request.user.id)
        user.avatar_key = file_key
        user.save()
        messages.add_message(request, messages.SUCCESS, "User avatar updated successfully.")
    except Exception as e:
        traceback.print_exception(e)
        messages.add_message(request, messages.ERROR, "Failed to save the new image location in database! Please try again.")

    return HttpResponseRedirect(reverse('accounts:profile'))
