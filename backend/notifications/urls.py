# backend/notifications/urls.py

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('greetings/', views.greeting_list, name='greeting-list'),
    path('greetings/<int:pk>/', views.greeting_detail, name='greeting-detail'),
    path('greetings/batch-delete/', views.greeting_batch_delete, name='greeting-batch-delete'),
    path('greetings/import/', views.import_greetings, name='greeting-import'),
    path('greetings/export/', views.export_greetings, name='greeting-export'),
    path('graduated-alumni/', views.graduated_alumni_list, name='graduated-alumni-list'),
]