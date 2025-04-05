from rest_framework import serializers
from .models import DonationProject


class DonationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationProject
        fields = ['id', 'name', 'type', 'purpose', 'target_amount',
                  'current_amount', 'donor_count', 'end_time']
