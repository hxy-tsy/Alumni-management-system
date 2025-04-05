from django.urls import path
from . import views

app_name = 'association'

urlpatterns = [
    path('general/', views.general_association_view, name='general-association'),
    path('branches/', views.branch_association_list, name='branch-list'),
    path('branches/<int:pk>/', views.branch_association_detail, name='branch-detail'),
    path('branches/<int:pk>/members/', views.association_members, name='branch-members'),
    path('branches/<int:pk>/apply/', views.apply_to_join, name='apply-to-join'),
    path('my-branch/', views.my_branch_view, name='my-branch'),
    path('my-branch/members/', views.my_branch_members, name='my-branch-members-list'),
    path('my-branch/members/add/', views.add_branch_member, name='add-branch-member'),
    path('my-branch/members/<int:pk>/update/', views.update_branch_member, name='update-branch-member'),
    path('my-branch/members/<int:pk>/delete/', views.delete_branch_member, name='delete-branch-member'),
    path('my-branch/members/batch-delete/', views.batch_delete_branch_members, name='batch-delete-branch-members'),
    path('my-branch/members/export/', views.export_branch_members, name='export-branch-members'),
    path('my-branch/members/import/', views.import_branch_members, name='import-branch-members'),
    path('my-branch/applications/', views.pending_applications, name='pending-applications'),
    path('my-branch/applications/<int:pk>/', views.handle_application, name='handle-application'),
    path('my-joined/', views.my_joined_association, name='my-joined-association'),
    path('upload/', views.upload_image, name='upload-image'),
    path('quit/<int:pk>/', views.quit_association, name='quit_association'),
]