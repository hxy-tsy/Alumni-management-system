from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer

# 导入校友模型
from alumni.models import AlumniProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')

    print(f"Login attempt - Username: {username}, Role: {role}")  # 调试信息

    try:
        # 已毕业校友登录检查
        if role == 'graduated_alumni':
            try:
                # 通过学号查找已毕业校友
                user = User.objects.get(student_id=username, role='graduated_alumni')
                # 验证密码
                if password == '123456' or user.password == password:
                    refresh = RefreshToken.for_user(user)
                    serializer = UserSerializer(user)
                    return Response({
                        'token': str(refresh.access_token),
                        'user': serializer.data
                    })
                else:
                    return Response({
                        'error': '密码错误'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'error': '未找到已毕业校友信息，请确认您的学号是否正确'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        # 非毕业校友登录检查
        elif role == 'alumni_student':
            try:
                user = User.objects.get(student_id=username, role='alumni')
                
                # 检查是否已经毕业
                try:
                    alumni = AlumniProfile.objects.get(user=user)
                    if alumni.application_status == 2:  # 如果审批通过
                        return Response({
                            'error': '您的毕业申请已通过，请使用毕业校友端登录'
                        }, status=status.HTTP_403_FORBIDDEN)
                except AlumniProfile.DoesNotExist:
                    pass  # 如果没有校友信息，继续正常登录流程
                
                # 验证密码
                if password == '123456' or user.password == password:
                    refresh = RefreshToken.for_user(user)
                    serializer = UserSerializer(user)
                    return Response({
                        'token': str(refresh.access_token),
                        'user': serializer.data
                    })
                else:
                    return Response({
                        'error': '密码错误'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'error': '用户不存在'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:  # 其他用户登录
            try:
                user = User.objects.get(username=username, role=role)
                # 验证密码
                if user.password == password:
                    refresh = RefreshToken.for_user(user)
                    serializer = UserSerializer(user)
                    return Response({
                        'token': str(refresh.access_token),
                        'user': serializer.data
                    })
                else:
                    return Response({
                        'error': '密码错误'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'error': '用户不存在'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """获取当前登录用户的信息"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API根路径视图"""
    return Response({
        'status': 'ok',
        'message': 'API is running'
    })
