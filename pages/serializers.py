# Local Apps
from .models import (
    Home,
    About,
)
from seo.serializers import BaseSeoSerializer
from utils.serializers import BaseStaticPageSerializer

# Third Party Packages
from rest_framework import serializers



class HomeDetailSerializer(BaseSeoSerializer):
    """Get home page detail."""


    class Meta:
        model = Home
        fields = (*BaseStaticPageSerializer.Meta.fields, 'video', *BaseSeoSerializer.Meta.fields)




class AboutDetailSerializer(BaseSeoSerializer):
    """Get about page detail."""


    class Meta:
        model = About
        fields = (*BaseStaticPageSerializer.Meta.fields, 'video', *BaseSeoSerializer.Meta.fields,)