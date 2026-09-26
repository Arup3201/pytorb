from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register", view=views.register_account, name='register'),
    path("login", view=views.login_account, name='login'),
    path("profile", view=views.profile, name='profile'),
    path("logout", view=views.account_logout, name='logout'),
    path("edit", view=views.edit_account, name='edit'),
    path("edit_avatar", view=views.edit_avatar, name='edit_avatar')
]