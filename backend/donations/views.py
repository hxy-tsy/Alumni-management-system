from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F
from .models import DonationProject
from .serializers import DonationProjectSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request):
    # 获取查询参数
    name = request.query_params.get('name', '')

    # 构建查询条件
    query = Q()
    if name:
        query &= Q(name__icontains=name)

    # 查询数据
    projects = DonationProject.objects.filter(query).order_by('-end_time')

    # 分页
    paginator = StandardResultsSetPagination()
    paginated_projects = paginator.paginate_queryset(projects, request)
    serializer = DonationProjectSerializer(paginated_projects, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_donate(request, project_id):
    try:
        # 获取项目
        project = DonationProject.objects.get(pk=project_id)
        
        # 获取捐赠金额
        amount = request.data.get('amount')
        if not amount or float(amount) <= 0:
            return Response(
                {'error': '请输入有效的捐赠金额'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 更新项目金额和捐赠人数
        project.current_amount = F('current_amount') + amount
        project.donor_count = F('donor_count') + 1
        project.save()

        # 重新获取更新后的项目数据
        project.refresh_from_db()
        
        return Response({
            'message': '捐赠成功',
            'current_amount': project.current_amount,
            'donor_count': project.donor_count
        })

    except DonationProject.DoesNotExist:
        return Response(
            {'error': '项目不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
