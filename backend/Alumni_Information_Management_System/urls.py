"""Alumni_Information_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 修改API路由前缀
    path('api/users/', include('users.urls')),
    path('api/alumni/', include('alumni.urls')),
    path('api/association/', include('association.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/donations/', include('donations.urls')),
    path('api/council/', include('council.urls')),
    # 添加根路径重定向
    path('', RedirectView.as_view(url='/api/')),
]

# 只在 DEBUG 模式下添加 debug_toolbar 的 URL
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# 添加媒体文件URL配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
