from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path("", view=views.list, name='list'),
    path("<int:pk>/", view=views.index, name='index'),
    path("edit/<int:pk>/", view=views.edit, name='edit'),
    path("<int:project_id>/tasks/", view=views.create_task, name='create_task')
]