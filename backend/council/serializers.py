from rest_framework import serializers
from .models import CouncilMeeting
from users.serializers import UserSerializer

class CouncilMeetingSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    invitees_info = UserSerializer(source='invitees', many=True, read_only=True)
    
    class Meta:
        model = CouncilMeeting
        fields = ['id', 'name', 'content', 'location', 'invitees', 'invitees_info',
                 'meeting_time', 'user', 'user_info', 'invitation_sent']
        read_only_fields = ['user', 'invitation_sent']

    def create(self, validated_data):
        # 获取当前用户作为召开人
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data) 