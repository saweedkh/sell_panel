# Local Apps
from .models import (
    Province,
    City,
)
from .serializers import (
    ProvinceListSerializer,
    CityListSerializer,
)

# Third Party Packages
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ProvinceListView(ListAPIView):
    """Get all provinces."""
    serializer_class = ProvinceListSerializer
    queryset = Province.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ('name',)


class CityListView(ListAPIView):
    """Get all cities."""
    serializer_class = CityListSerializer
    queryset = City.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend,)
    filterset_fields = ('province',)
    ordering_fields = ('name',)

