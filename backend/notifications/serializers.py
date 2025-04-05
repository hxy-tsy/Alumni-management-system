# backend/notifications/serializers.py

from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender_info = UserSerializer(source='sender', read_only=True)
    receivers_info = UserSerializer(source='receivers', many=True, read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'type', 'type_display', 'sender', 
                 'sender_info', 'receivers', 'receivers_info', 
                 'send_time', 'status', 'status_display']
        read_only_fields = ['sender']