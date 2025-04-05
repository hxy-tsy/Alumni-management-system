from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone', 'gender', 'department', 'graduation_year', 'is_graduated']
        read_only_fields = ['id']
        extra_kwargs = {
            'username': {'validators': []}
        }
