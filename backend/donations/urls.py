from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:project_id>/donate/', views.project_donate, name='project-donate'),
]