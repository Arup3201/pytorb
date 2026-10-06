from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("", view=views.create_task, name='create')
]