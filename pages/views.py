# Local Apps
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import requests
from .serializers import (
    HomeDetailSerializer,
    AboutDetailSerializer,
)
from . import default_pages

# Third Party Packages
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

import xmltodict


import xml.etree.ElementTree as ET

class HomePageDetailView(RetrieveAPIView):
    """Get home page detail."""

    serializer_class = HomeDetailSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_object(self):
        obj = default_pages.get_or_create_home_page()
        self.check_object_permissions(self.request, obj)
        return obj


class AboutPageDetailView(RetrieveAPIView):
    """Get about page detail."""

    serializer_class = AboutDetailSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_object(self):
        obj = default_pages.get_or_create_about_us_page()
        self.check_object_permissions(self.request, obj)
        return obj

    
class SiteMapView(APIView):
    def get(self, request):
        protocol = request.scheme
        reverse_url = reverse('django.contrib.sitemaps.views.sitemap')
        
        url = f'{protocol}://{settings.SITE_DOMAIN}{reverse_url}' 
        response = requests.get(url)
        
        if response.status_code == 200:
            xml_content = response.content
            xml_dict = xmltodict.parse(xml_content)
            return JsonResponse(xml_dict)
        else:
            return JsonResponse({'error': 'Unable to fetch sitemap'}, status=500)
