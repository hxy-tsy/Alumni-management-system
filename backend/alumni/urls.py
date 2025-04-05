from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'alumni', views.AlumniViewSet)
router.register(r'applications', views.ApplicationViewSet, basename='alumni-applications')

urlpatterns = [
    # 先注册路由器的 URL
    path('', include(router.urls)),
    # 其他 URL 模式
    path('list/', views.alumni_list, name='alumni-list'),  # 修改这个路径避免冲突
    path('add/', views.alumni_list, name='alumni-create'),  # 添加这个路径用于创建校友
    path('current/', views.current_alumni, name='current-alumni'),
    path('detail/<int:pk>/', views.alumni_detail, name='alumni-detail'),
    path('batch-delete/', views.alumni_batch_delete, name='alumni-batch-delete'),
    path('upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('import/', views.import_alumni, name='import-alumni'),
    path('export/', views.export_alumni, name='export-alumni'),
    path('apply-graduation/', views.apply_graduation, name='apply-graduation'),
    path('approve-application/<int:pk>/', views.approve_application, name='approve-application'),
    path('reject-application/<int:pk>/', views.reject_application, name='reject-application'),
    path('statistics/', views.statistics, name='alumni-statistics'),
    # 添加毕业去向数据分析路由
    path('career-recommendation-data/', views.career_recommendation_data, name='career-recommendation-data'),
] 