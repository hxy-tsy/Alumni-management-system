from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Association, AssociationMember
from .serializers import AssociationSerializer, AssociationMemberSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
import pandas as pd
import io
from rest_framework import serializers


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def general_association_view(request):
    """获取或更新总会信息"""
    try:
        association = Association.objects.get(type='general')
    except Association.DoesNotExist:
        return Response({"error": "总会不存在"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssociationSerializer(association)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AssociationSerializer(association, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def branch_association_list(request):
    """
    获取分会列表或创建新分会
    """
    if request.method == 'GET':
        # 获取查询参数
        name = request.query_params.get('name', '')
        type = request.query_params.get('type', '')

        # 构建查询条件
        query = ~Q(type='general')  # 排除总会
        if name:
            query &= Q(name__icontains=name)
        if type:
            query &= Q(type=type)
        branches = Association.objects.filter(query)
        serializer = AssociationSerializer(branches, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AssociationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def branch_association_detail(request, pk):
    """
    获取、更新特定分会
    """
    branch = get_object_or_404(Association, pk=pk)

    if branch.type == 'general':
        return Response({"error": "不能通过此接口操作总会"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = AssociationSerializer(branch)
        print(f"返回分会详情: {serializer.data}")
        return Response(serializer.data)

    elif request.method == 'PUT':
        print("收到PUT请求，数据:", request.data)

        # 检查必填字段
        required_fields = ['name', 'founding_date']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            error_msg = f"缺少必填字段: {', '.join(missing_fields)}"
            print(error_msg)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssociationSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                # 重新获取更新后的数据，包括成员信息
                updated_serializer = AssociationSerializer(branch)
                return Response(updated_serializer.data)
            except Exception as e:
                print(f"保存时发生错误: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("序列化器验证失败，错误:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_image(request):
    """
    上传校友会图片
    """
    parser_classes = (MultiPartParser, FormParser)
    print("*****************************")
    if 'file' not in request.FILES:
        return Response({"error": "没有提供文件"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # 验证文件类型
    if not file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return Response({"error": "只允许上传图片文件"}, status=status.HTTP_400_BAD_REQUEST)

    # 验证文件大小
    if file.size > 2 * 1024 * 1024:  # 2MB
        return Response({"error": "文件大小不能超过2MB"}, status=status.HTTP_400_BAD_REQUEST)

    # 保存文件
    file_path = os.path.join('association_images', file.name)
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print("图片上传到了:", full_path)

    # 确保目录存在
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # 返回文件URL（确保URL格式正确）
    file_url = os.path.join(settings.MEDIA_URL, file_path)

    # 确保URL以/开头
    if not file_url.startswith('/'):
        file_url = '/' + file_url

    print(f"上传图片成功，URL: {file_url}")

    return Response({"url": file_url}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def association_members(request, pk):
    """
    获取特定分会的成员列表
    """
    association = get_object_or_404(Association, pk=pk)
    members = AssociationMember.objects.filter(association=association)
    serializer = AssociationMemberSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_branch_view(request):
    """
    获取或更新校友联络人管理的校友会分会信息
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    if request.method == 'GET':
        serializer = AssociationSerializer(branch)
        return Response(serializer.data)

    elif request.method == 'PUT':
        print("校友联络人更新分会信息，数据:", request.data)

        # 检查必填字段
        required_fields = ['name', 'founding_date']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            error_msg = f"缺少必填字段: {', '.join(missing_fields)}"
            print(error_msg)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssociationSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                # 重新获取更新后的数据
                updated_serializer = AssociationSerializer(branch)
                return Response(updated_serializer.data)
            except Exception as e:
                print(f"保存时发生错误: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("序列化器验证失败，错误:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_branch_members(request):
    """
    获取当前校友联络员管理的分会成员列表
    """
    # 确保用户是校友联络员
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络员可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # 查找校友联络员管理的分会
        association = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        association = Association.objects.filter(leader=request.user).first()
    
    # 获取查询参数
    student_id = request.query_params.get('student_id', '')
    name = request.query_params.get('name', '')
    department = request.query_params.get('department', '')
    class_name = request.query_params.get('class_name', '')
    
    # 构建查询条件
    members = AssociationMember.objects.filter(association=association)
    
    if student_id:
        members = members.filter(
            Q(user__student_id__icontains=student_id) |
            Q(profile__student_id__icontains=student_id)
        )
    
    if name:
        members = members.filter(
            Q(user__first_name__icontains=name) |
            Q(user__last_name__icontains=name) |
            Q(user__username__icontains=name)
        )
    
    if department:
        members = members.filter(user__department__icontains=department)
    
    if class_name:
        members = members.filter(profile__class_name__icontains=class_name)
    
    # 分页
    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('page_size', 10))
    result_page = paginator.paginate_queryset(members, request)
    
    serializer = AssociationMemberSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_branch_member(request):
    """
    添加校友会分会成员
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    # 获取请求数据
    student_id = request.data.get('student_id')
    name = request.data.get('name')
    phone = request.data.get('phone')
    department = request.data.get('department')
    class_name = request.data.get('class_name')
    birth_date = request.data.get('birth_date')
    graduation_date = request.data.get('graduation_date')
    current_company = request.data.get('current_company')

    # 验证必填字段
    if not student_id or not name:
        return Response({"error": "学号和姓名为必填字段"}, status=status.HTTP_400_BAD_REQUEST)

    # 查找或创建用户
    try:
        # 先尝试通过学号查找校友档案
        alumni_profile = AlumniProfile.objects.get(student_id=student_id)
        user = alumni_profile.user
    except AlumniProfile.DoesNotExist:
        # 如果找不到校友档案，则创建新用户和档案
        # 分割姓名
        if len(name) > 1:
            first_name = name[0]
            last_name = name[1:]
        else:
            first_name = name
            last_name = ""

        # 创建用户
        user = User.objects.create(
            username=student_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            department=department,
            role='alumni',
            is_graduated=True
        )

        # 创建校友档案
        alumni_profile = AlumniProfile.objects.create(
            user=user,
            student_id=student_id,
            class_name=class_name,
            birth_date=birth_date,
            graduation_date=graduation_date,
            current_company=current_company,
            is_graduated=1  # 已毕业
        )

    # 检查用户是否已经是分会成员
    if AssociationMember.objects.filter(association=branch, user=user).exists():
        return Response({"error": "该用户已经是分会成员"}, status=status.HTTP_400_BAD_REQUEST)

    # 创建分会成员关系
    member = AssociationMember.objects.create(
        association=branch,
        user=user,
        role='member'  # 默认为普通成员
    )

    serializer = AssociationMemberSerializer(member)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_branch_member(request, pk):
    """
    更新校友会分会成员信息
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    # 查找成员
    try:
        member = AssociationMember.objects.get(pk=pk, association=branch)
    except AssociationMember.DoesNotExist:
        return Response({"error": "成员不存在或不属于您管理的分会"}, status=status.HTTP_404_NOT_FOUND)

    # 获取请求数据
    name = request.data.get('name')
    phone = request.data.get('phone')
    department = request.data.get('department')
    class_name = request.data.get('class_name')
    birth_date = request.data.get('birth_date')
    graduation_date = request.data.get('graduation_date')
    current_company = request.data.get('current_company')

    # 更新用户信息
    user = member.user

    if name:
        # 分割姓名
        if len(name) > 1:
            user.first_name = name[0]
            user.last_name = name[1:]
        else:
            user.first_name = name
            user.last_name = ""

    if phone:
        user.phone = phone

    if department:
        user.department = department

    user.save()

    # 更新校友档案
    try:
        profile = AlumniProfile.objects.get(user=user)

        if class_name:
            profile.class_name = class_name

        if birth_date:
            profile.birth_date = birth_date

        if graduation_date:
            profile.graduation_date = graduation_date

        if current_company:
            profile.current_company = current_company

        profile.save()
    except AlumniProfile.DoesNotExist:
        # 如果没有校友档案，则创建一个
        AlumniProfile.objects.create(
            user=user,
            student_id=user.username,
            class_name=class_name or "",
            birth_date=birth_date,
            graduation_date=graduation_date,
            current_company=current_company or "",
            is_graduated=1  # 已毕业
        )

    serializer = AssociationMemberSerializer(member)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_branch_member(request, pk):
    """
    删除校友会分会成员
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        # todo 就算有多个分会，删除对应分会的记录就行了，而不是取第一个这么简单
        branch = Association.objects.filter(leader=request.user).first()

    # 查找成员
    try:
        member = AssociationMember.objects.get(pk=pk, association=branch)
    except AssociationMember.DoesNotExist:
        return Response({"error": "成员不存在或不属于您管理的分会"}, status=status.HTTP_404_NOT_FOUND)

    # 删除成员关系（不删除用户和校友档案）
    member.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_delete_branch_members(request):
    """
    批量删除校友会分会成员
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    # 获取要删除的成员ID列表
    ids = request.data.get('ids', [])

    if not ids:
        return Response({"error": "未提供要删除的成员ID"}, status=status.HTTP_400_BAD_REQUEST)

    # 删除成员关系
    deleted_count = AssociationMember.objects.filter(pk__in=ids, association=branch).delete()[0]

    return Response({"deleted_count": deleted_count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_branch_members(request):
    """
    导出校友会分会成员列表
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    # 获取分会成员
    members = AssociationMember.objects.filter(association=branch)

    # 应用搜索过滤
    student_id = request.query_params.get('student_id', None)
    name = request.query_params.get('name', None)
    department = request.query_params.get('department', None)
    class_name = request.query_params.get('class_name', None)

    if student_id:
        members = members.filter(user__alumni_profile__student_id__icontains=student_id)

    if name:
        members = members.filter(
            Q(user__first_name__icontains=name) |
            Q(user__last_name__icontains=name) |
            Q(user__username__icontains=name)
        )

    if department:
        members = members.filter(user__department__icontains=department)

    if class_name:
        members = members.filter(user__alumni_profile__class_name__icontains=class_name)

    # 准备导出数据
    data = []
    for member in members:
        user = member.user
        try:
            profile = AlumniProfile.objects.get(user=user)
            student_id = profile.student_id
            class_name = profile.class_name
            birth_date = profile.birth_date
            graduation_date = profile.graduation_date
            current_company = profile.current_company
        except AlumniProfile.DoesNotExist:
            student_id = user.username
            class_name = ""
            birth_date = None
            graduation_date = None
            current_company = ""

        data.append({
            '学号': student_id,
            '姓名': user.first_name + user.last_name,
            '电话': user.phone,
            '学院': user.department,
            '班级': class_name,
            '出生日期': birth_date,
            '毕业时间': graduation_date,
            '毕业去向': current_company,
            '加入时间': member.join_date
        })

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 创建Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='校友会成员', index=False)

    # 设置响应头
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=校友会成员列表.xlsx'

    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_branch_members(request):
    """
    导入校友会分会成员
    """
    # 确保用户是校友联络人
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络人可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # 查找校友联络人管理的分会
        branch = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会分会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个分会，取第一个
        branch = Association.objects.filter(leader=request.user).first()

    # 检查是否上传了文件
    if 'file' not in request.FILES:
        return Response({"error": "未上传文件"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # 读取Excel文件
    try:
        df = pd.read_excel(file)
    except Exception as e:
        return Response({"error": f"读取文件失败: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # 检查必要的列
    required_columns = ['学号', '姓名']
    for column in required_columns:
        if column not in df.columns:
            return Response({"error": f"文件缺少必要的列: {column}"}, status=status.HTTP_400_BAD_REQUEST)

    # 导入成员
    success_count = 0
    errors = []

    for _, row in df.iterrows():
        try:
            student_id = str(row['学号'])
            name = str(row['姓名'])

            # 获取其他字段（如果存在）
            phone = str(row.get('电话', '')) if pd.notna(row.get('电话', '')) else ''
            department = str(row.get('学院', '')) if pd.notna(row.get('学院', '')) else ''
            class_name = str(row.get('班级', '')) if pd.notna(row.get('班级', '')) else ''
            birth_date = row.get('出生日期', None) if pd.notna(row.get('出生日期', None)) else None
            graduation_date = row.get('毕业时间', None) if pd.notna(row.get('毕业时间', None)) else None
            current_company = str(row.get('毕业去向', '')) if pd.notna(row.get('毕业去向', '')) else ''

            # 查找或创建用户
            try:
                # 先尝试通过学号查找校友档案
                alumni_profile = AlumniProfile.objects.get(student_id=student_id)
                user = alumni_profile.user
            except AlumniProfile.DoesNotExist:
                # 如果找不到校友档案，则创建新用户和档案
                # 分割姓名
                if len(name) > 1:
                    first_name = name[0]
                    last_name = name[1:]
                else:
                    first_name = name
                    last_name = ""

                # 创建用户
                user = User.objects.create(
                    username=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    department=department,
                    role='alumni',
                    is_graduated=True
                )

                # 创建校友档案
                alumni_profile = AlumniProfile.objects.create(
                    user=user,
                    student_id=student_id,
                    class_name=class_name,
                    birth_date=birth_date,
                    graduation_date=graduation_date,
                    current_company=current_company,
                    is_graduated=1  # 已毕业
                )

            # 检查用户是否已经是分会成员
            if not AssociationMember.objects.filter(association=branch, user=user).exists():
                # 创建分会成员关系
                AssociationMember.objects.create(
                    association=branch,
                    user=user,
                    role='member'  # 默认为普通成员
                )
                success_count += 1

        except Exception as e:
            errors.append(f"导入行 {_ + 2} 失败: {str(e)}")

    return Response({
        "success": True,
        "count": success_count,
        "errors": errors
    })


@api_view(['GET'])
def my_joined_association(request):
    """
    获取当前用户相关的所有校友会信息（包括已加入、审核中、被拒绝的）
    """
    # 确保用户是已毕业校友
    if request.user.role != 'graduated_alumni' or not request.user.is_graduated:
        return Response({"error": "只有已毕业校友可以访问此接口"}, status=status.HTTP_403_FORBIDDEN)

    # 查找用户相关的所有校友会记录
    members = AssociationMember.objects.filter(user=request.user)
    
    # 使用自定义的序列化器，包含状态信息
    class MyAssociationMemberSerializer(serializers.ModelSerializer):
        association_name = serializers.CharField(source='association.name')
        association_type = serializers.CharField(source='association.type')
        association_type_display = serializers.CharField(source='association.get_type_display')
        leader_name = serializers.SerializerMethodField()
        status_display = serializers.CharField(source='get_status_display')
        join_date = serializers.DateField()
        founding_date = serializers.DateField(source='association.founding_date')
        
        class Meta:
            model = AssociationMember
            fields = ['id', 'association_name', 'association_type', 'association_type_display', 
                     'leader_name', 'status', 'status_display', 'join_date', 'founding_date']
        
        def get_leader_name(self, obj):
            leader = obj.association.leader
            if leader:
                return f"{leader.first_name}{leader.last_name}"
            return ""

    serializer = MyAssociationMemberSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def apply_to_join(request, pk):
    """
    申请加入校友会
    """
    # 确保用户是已毕业校友
    if request.user.role != 'graduated_alumni' or not request.user.is_graduated:
        return Response({"error": "只有已毕业校友可以申请加入校友会"}, status=status.HTTP_403_FORBIDDEN)

    # 查找校友会
    try:
        association = Association.objects.get(pk=pk)
    except Association.DoesNotExist:
        return Response({"error": "校友会不存在"}, status=status.HTTP_404_NOT_FOUND)

    # 检查用户是否已经是该校友会的成员或已经申请过
    existing_member = AssociationMember.objects.filter(association=association, user=request.user).first()
    if existing_member:
        if existing_member.status == 0 or existing_member.status == 2:
            return Response({"error": "您已经是该校友会的成员"}, status=status.HTTP_400_BAD_REQUEST)
        elif existing_member.status == 1:
            return Response({"error": "您已经申请加入该校友会，请等待审批"}, status=status.HTTP_400_BAD_REQUEST)
        elif existing_member.status == 3:
            # 如果之前被拒绝，可以重新申请
            existing_member.status = 1
            existing_member.save()
            return Response({"message": "申请已提交，请等待审批"}, status=status.HTTP_200_OK)

    # 创建申请记录
    member = AssociationMember(
        association=association,
        user=request.user,
        role='member',
        status=1  # 申请中
    )
    member.save()

    return Response({"message": "申请已提交，请等待审批"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_applications(request):
    """
    获取待审批的申请列表
    """
    # 确保用户是校友联络员
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络员可以查看申请列表"}, status=status.HTTP_403_FORBIDDEN)

    # 查找用户管理的校友会
    try:
        association = Association.objects.get(leader=request.user)
    except Association.DoesNotExist:
        return Response({"error": "您尚未管理任何校友会"}, status=status.HTTP_404_NOT_FOUND)
    except Association.MultipleObjectsReturned:
        # 如果有多个校友会，取第一个
        association = Association.objects.filter(leader=request.user).first()

    # 查找待审批的申请
    pending_members = AssociationMember.objects.filter(association=association, status=1)
    serializer = AssociationMemberSerializer(pending_members, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def handle_application(request, pk):
    """
    处理加入申请（通过或拒绝）
    """
    # 确保用户是校友联络员
    if request.user.role != 'liaison':
        return Response({"error": "只有校友联络员可以处理申请"}, status=status.HTTP_403_FORBIDDEN)
    
    # 查找申请记录
    try:
        member = AssociationMember.objects.get(pk=pk)
    except AssociationMember.DoesNotExist:
        return Response({"error": "申请记录不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    # 确保是用户管理的校友会的申请
    if member.association.leader != request.user:
        return Response({"error": "您无权处理此申请"}, status=status.HTTP_403_FORBIDDEN)
    
    # 获取操作类型（通过或拒绝）
    action = request.data.get('action')
    if action not in ['approve', 'reject']:
        return Response({"error": "无效的操作类型，必须是 'approve' 或 'reject'"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查当前状态是否允许操作
    if member.status == 2:  # 已通过
        return Response({"error": "此申请已经通过，无法再次处理"}, status=status.HTTP_400_BAD_REQUEST)
    elif member.status == 3 and action == 'reject':  # 已拒绝且尝试再次拒绝
        return Response({"error": "此申请已经被拒绝，无法再次拒绝"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 处理申请
    if action == 'approve':
        member.status = 2  # 已通过
        message = "申请已通过"
    else:
        member.status = 3  # 已拒绝
        message = "申请已拒绝"
    
    member.save()
    
    return Response({"message": message}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def quit_association(request, pk):
    """
    退出校友会
    """
    try:
        # 查找成员记录
        member = AssociationMember.objects.get(
            id=pk,
            user=request.user
        )
        
        # 检查状态是否为已通过
        if member.status != 2:
            return Response({"error": "只有已加入的校友会才能退出"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 删除成员记录
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except AssociationMember.DoesNotExist:
        return Response({"error": "未找到相关记录"}, status=status.HTTP_404_NOT_FOUND)
