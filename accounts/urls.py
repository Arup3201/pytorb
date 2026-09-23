from django.urls import path
from . import views

urlpatterns = [
    path("register", view=views.register, name='register'),
    path("login", view=views.login, name='login'),
    path("profile", view=views.profile, name='profile'),
]