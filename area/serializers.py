# Local Apps
from .models import (
    Province,
    City
)

# Third Party Packages
from rest_framework import serializers


class ProvinceListSerializer(serializers.ModelSerializer):
    """Get list of all provinces."""

    class Meta:
        model = Province
        fields = ('id', 'name',)


class CityListSerializer(serializers.ModelSerializer):
    """Get list of all cities."""

    class Meta:
        model = City
        fields = ('id', 'province', 'name',)
