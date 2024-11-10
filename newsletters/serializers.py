# Local Apps
from .models import Member

# Third Party Packages
from rest_framework import serializers


class MemberCreateSerializer(serializers.ModelSerializer):
    """Create member for newsletters."""

    class Meta:
        model = Member
        fields = ('email',)
