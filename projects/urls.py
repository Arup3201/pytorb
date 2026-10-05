from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path("", view=views.list, name='list'),
    path("<int:pk>/", view=views.index, name='index')
]