from rest_framework import serializers
from .models import Activity, ActivityMember, ActivityFeedback
from users.serializers import UserSerializer

class ActivitySerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    organization = serializers.CharField(required=False, allow_null=True)
    venue = serializers.CharField(required=False, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    registration_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'applicant_name', 'phone', 'organization',
                 'venue', 'apply_time', 'event_time', 'status', 'status_display',
                 'registration_count', 'is_registered']
        read_only_fields = ('apply_time', 'status')

    def get_registration_count(self, obj):
        return obj.members.count()

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class ActivityMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = ActivityMember
        fields= ['id', 'user', 'activity', 'status', 'status_display']


class ActivityFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ActivityFeedback
        fields = ['id', 'activity', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']