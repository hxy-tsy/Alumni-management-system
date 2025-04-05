from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views


@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'API is running'
    })


urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('login/', views.login, name='login'),
    # path('register/', views.register, name='register'),
    path('current-user/', views.current_user, name='current-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
