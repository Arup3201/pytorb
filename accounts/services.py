from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from . import models

def create_user(*, email: str, username: str, first_name: str | None, last_name: str|None, password: str):
    try:
        user = models.User(email=email, username=username)
        user.first_name = first_name or ""
        user.last_name = last_name or ""
        user.set_password(password)
        user.save()
    except KeyError:
        raise ValueError("Mandatory fields: email, username and password.")
    except IntegrityError:
        raise ValueError("Username/Email already exists in the database.")

def login_user(*, request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise ValueError("Username/Password is wrong.")
    
    login(request, user)

def logout_user(*, request):
    logout(request)

def edit_account(*, user: models.User, first_name: str, last_name: str, skills: str):
    user = models.User.objects.get(id=user.pk)
    user.first_name = first_name
    user.last_name = last_name
    user.skills = skills
    user.save()

def save_user_avatar(*, user: models.User, file):
    file_key = f"users/{user.pk}/avatars/{file.name}"
    default_storage.save(file_key, file)
    
    user = models.User.objects.get(id=user.pk)
    user.avatar_key = file_key
    user.save()
