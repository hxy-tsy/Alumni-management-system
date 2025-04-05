from rest_framework import serializers
from .models import Association, AssociationMember
from django.core.files.base import ContentFile
from users.models import User
from alumni.models import AlumniProfile
import base64
import os
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'department']


class AlumniProfileSerializer(serializers.ModelSerializer):
    # 添加自定义字段
    department = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    
    class Meta:
        model = AlumniProfile
        fields = ['student_id', 'department', 'class_name', 'graduation_date', 'current_company', 'position', 'phone']
    
    def get_department(self, obj):
        # 从用户表获取部门信息
        if hasattr(obj.user, 'department'):
            return obj.user.department
        return obj.major  # 如果用户表没有部门信息，则返回专业作为备选
    
    def get_phone(self, obj):
        # 从用户表获取电话信息
        if hasattr(obj.user, 'phone'):
            return obj.user.phone
        return None


class AssociationMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AssociationMember
        fields = ['id', 'user', 'profile', 'role', 'role_display', 'join_date', 'status', 'status_display']
    
    def get_profile(self, obj):
        try:
            profile = AlumniProfile.objects.get(user=obj.user)
            serializer = AlumniProfileSerializer(profile)
            data = serializer.data
            
            # 直接从 User 模型获取 department 和 phone 字段
            data['department'] = obj.user.department
            data['phone'] = obj.user.phone
            
            print(f"Profile data for user {obj.user.username}: {data}")
            return data
        except AlumniProfile.DoesNotExist:
            # 如果没有找到 AlumniProfile，则创建一个只包含 User 信息的数据
            return {
                'student_id': obj.user.student_id,
                'department': obj.user.department,
                'phone': obj.user.phone,
                'class_name': '',
                'graduation_date': None,
                'current_company': '',
                'position': ''
            }


class AssociationSerializer(serializers.ModelSerializer):
    # 添加一个字段用于接收图片路径
    image_path = serializers.CharField(required=False, write_only=True)
    members_info = serializers.SerializerMethodField()
    # 将image从SerializerMethodField改为标准字段
    image = serializers.CharField(required=False)
    
    class Meta:
        model = Association
        fields = ['id', 'name', 'type', 'description', 'founding_date', 'leader', 'image', 'image_path', 'members_info']
        read_only_fields = ['type']  # 类型不允许修改
        extra_kwargs = {
            'leader': {'required': False},  # 会长字段在更新时不是必需的
            'image': {'required': False},   # 图片字段不是必需的
        }
    
    def get_members_info(self, obj):
        members = AssociationMember.objects.filter(association=obj)
        return AssociationMemberSerializer(members, many=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.image:
            # 移除开头的 /media/ 如果存在
            image_url = str(instance.image.url)
            if image_url.startswith('/media/media/'):
                image_url = '/media/' + image_url.split('/media/media/')[1]
            ret['image'] = image_url
        return ret
        
    def to_internal_value(self, data):
        # 打印接收到的数据，用于调试
        print("序列化器接收到的数据:", data)

        # 创建一个新的数据字典，避免修改原始数据
        processed_data = data.copy()

        # 直接处理图片路径
        if 'image' in processed_data and isinstance(processed_data['image'], str):
            # 如果不是base64编码的图片数据
            if not processed_data['image'].startswith('data:'):
                # 将路径规范化（替换反斜杠为正斜杠）
                image_path = processed_data['image'].replace('\\', '/')
                # 如果路径以/media/开头，去掉这个前缀
                if image_path.startswith('/media/'):
                    image_path = image_path[7:]  # 去掉'/media/'前缀
                print(f"处理后的图片路径: {image_path}")
                # 直接设置为相对路径
                processed_data['image'] = image_path
            else:
                print("收到了base64编码的图片数据")

        # 使用处理后的数据调用父类方法
        validated_data = super().to_internal_value(processed_data)
        print("验证后的数据:", validated_data)
        return validated_data
    
    def update(self, instance, validated_data):
        print("更新字段:", validated_data)
        
        # 更新所有字段
        for attr, value in validated_data.items():
            print(f"更新字段 {attr}: {value}")
            setattr(instance, attr, value)
        
        # 保存实例
        instance.save()
        print(f"保存后的实例: {instance.__dict__}")
        return instance