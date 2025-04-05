from rest_framework import serializers
from .models import AlumniProfile, AlumniApplication
from users.models import User
from users.serializers import UserSerializer


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'phone', 'department', 'student_id', 'avatar']
#         extra_kwargs = {
#             'username': {'validators': []},
#             'password': {'write_only': True},
#         }


class AlumniProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = AlumniProfile
        fields = '__all__'
        extra_kwargs = {
            'education_level': {'required': False},
            'major': {'required': False},
            'graduation_date': {'required': False},
            'current_company': {'required': False},
            'position': {'required': False},
            'work_city': {'required': False},
            'address': {'required': False},
            'ethnicity': {'required': False},
            'gender': {'required': False},
            'birth_date': {'required': False},
            'student_id': {'required': False},
            'avatar': {'required': False, 'allow_null': True}
        }

    def to_internal_value(self, data):
        # 处理空字符串日期
        if 'birth_date' in data and data['birth_date'] == '':
            data['birth_date'] = None
        if 'graduation_date' in data and data['graduation_date'] == '':
            data['graduation_date'] = None
        
        # 处理头像字段
        if 'avatar' in data and isinstance(data['avatar'], str):
            if data['avatar'].startswith('/media/'):
                # 从路径中提取文件名
                data['avatar'] = data['avatar'].replace('/media/', '', 1)
        
        return super().to_internal_value(data)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # 添加默认密码和角色
        user_data['password'] = '123456'
        user_data['role'] = 'alumni'
        user_data['student_id'] = validated_data['student_id']
        # 使用 UserSerializer 创建用户
        user = UserSerializer().create(user_data)
        alumni = AlumniProfile.objects.create(user=user, **validated_data)
        return alumni

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer()
            user_serializer.update(instance.user, user_data)
        
        # 更新其他字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 确保返回完整的头像URL
        if data.get('avatar'):
            if not data['avatar'].startswith('http') and not data['avatar'].startswith('/'):
                data['avatar'] = f"/media/{data['avatar']}"
        return data


class AlumniApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AlumniProfile
        fields = '__all__'
