# Django Build-in
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

# Local Apps
from .models import SiteGlobalSetting, SocialMediaSetting
from .serializers import GlobalSettingSerializers, SocialMediaSerializers


class GlobalSettingDetailView(RetrieveAPIView):
    """Get site global settings."""
    serializer_class = GlobalSettingSerializers
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_object(self):
        obj = SiteGlobalSetting.get_default_setting()
        return obj
