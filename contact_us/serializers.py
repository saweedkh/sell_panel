# Local Apps
from .models import ContactUsMessages
from setting.models import (
    SiteGlobalSetting,
    SocialMediaSetting,
)
from setting.serializers import (
    SocialMediaSerializers,
)

# Third Party Packages
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class ContactUsMessagesSerializer(serializers.ModelSerializer):
    """Submit message for contact."""

    class Meta:
        model = ContactUsMessages
        fields = ('type', 'fullname', 'phone', 'email', 'subject', 'message',)


class ContactUsDetailSerializer(serializers.ModelSerializer):
    """List of all contact ways."""

    socials = serializers.SerializerMethodField()

    class Meta:
        model = SiteGlobalSetting
        fields = ('phone', 'fax', 'email', 'address', 'map', 'longitude', 'latitude', 'zoom', 'socials',
                  )

    @extend_schema_field(SocialMediaSerializers)
    def get_socials(self, obj):
        return SocialMediaSerializers(instance=SocialMediaSetting.objects.all(), many=True, read_only=True,
                                      context=self.context).data

