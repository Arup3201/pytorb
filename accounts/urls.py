from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", view=views.register, name='register'),
    path("login/", view=views.login, name='login'),
    path("profile/", view=views.profile, name='profile'),
    path("logout/", view=views.account_logout, name='logout'),
    path("edit/", view=views.edit_account, name='edit'),
    path("upload_avatar/", view=views.upload_avatar, name='upload_avatar')
]