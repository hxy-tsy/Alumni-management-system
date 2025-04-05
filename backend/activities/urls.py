from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('list/', views.activity_list, name='activity-list'),
    path('add/', views.activity_list, name='activity-create'),  # 添加这个路径用于创建活动
    path('<int:pk>/', views.activity_detail, name='activity-detail'),
    path('batch-delete/', views.activity_batch_delete, name='activity-batch-delete'),
    path('import/', views.import_activities, name='activity-import'),
    path('export/', views.export_activities, name='activity-export'),
    path('<int:pk>/approve/', views.approve_activity, name='activity-approve'),
    path('<int:pk>/reject/', views.reject_activity, name='activity-reject'),
    path('<int:pk>/reapply/', views.reapply_activity, name='activity-reapply'),
    path('registration/list/', views.activity_registration_list, name='activity-registration-list'),
    path('<int:pk>/register/', views.register_activity, name='activity-register'),
    path('my-activities/', views.my_activities, name='my-activities'),
    path('cancel-registration/<int:pk>/', views.cancel_registration, name='cancel_registration'),
    path('planning/stats/', views.activity_planning_stats, name='activity_planning_stats'),
    path('feedback/<int:pk>/', views.submit_feedback, name='submit_feedback'),
    path('feedback/<int:pk>/get/', views.get_feedback, name='get_feedback'),
]
