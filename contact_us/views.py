# Local Apps
from .models import ContactUsMessages
from .serializers import (
    ContactUsMessagesSerializer,
    ContactUsDetailSerializer,
)
from setting.models import SiteGlobalSetting

# Third Party Packages
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)


class ContactUsMessageCreateView(CreateAPIView):
    """Submit message for contact."""
    serializer_class = ContactUsMessagesSerializer
    queryset = ContactUsMessages.objects.all()


class ContactUsDetailView(RetrieveAPIView):
    """List of all contact ways."""
    serializer_class = ContactUsDetailSerializer
    pagination_class = None

    def get_object(self):
        obj = SiteGlobalSetting.get_default_setting()
        return obj
