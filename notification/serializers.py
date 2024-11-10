from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import Notification

# Third Party Packages
from rest_framework import serializers


class ListNotificationSerializers(serializers.ModelSerializer):
    """ Show Notification List """
    
    class Meta:
        model = Notification
        fields = (
            'pk', 
            'user', 
            'text', 
            'is_read',
            'created',
            'updated',
        )
        read_only_fields = ('pk', 'created', 'updated')
