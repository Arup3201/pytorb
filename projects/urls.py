from django.urls import path, include
from . import views
from tasks import views as task_views

app_name = "projects"
urlpatterns = [
    path("", view=views.list, name='list'),
    path("explore/", view=views.get_projects_for_user, name='get_projects_for_user'),
    path("<int:pk>/", include([
        path("", view=views.index, name='index'),
        path("edit/", view=views.edit, name='edit'),
        path("tasks/", include([
            path("", view=task_views.create_task, name='create_task')
        ]))
    ])),
]