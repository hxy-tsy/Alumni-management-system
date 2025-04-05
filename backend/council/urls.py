from django.urls import path
from . import views

app_name = 'council'

urlpatterns = [
    path('meetings/', views.meeting_list, name='meeting-list'),
    path('meetings/<int:pk>/', views.meeting_detail, name='meeting-detail'),
    path('meetings/batch-delete/', views.meeting_batch_delete, name='meeting-batch-delete'),
    path('meetings/<int:pk>/send-invitation/', views.send_invitation, name='send-invitation'),
    path('meetings/<int:pk>/withdraw-invitation/', views.withdraw_invitation, name='withdraw-invitation'),
    path('meetings/import/', views.import_meetings, name='import-meetings'),
    path('meetings/export/', views.export_meetings, name='export-meetings'),
    path('graduated-alumni/', views.get_graduated_alumni, name='graduated-alumni'),
] 