# Local Apps
from .models import (
    SiteGlobalSetting,
    SocialMediaSetting,
)

# Third Party Packages
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from modeltranslation.translator import TranslationOptions


class SocialMediaSerializers(serializers.ModelSerializer):
    """Get all social media."""

    class Meta:
        model = SocialMediaSetting
        fields = (
            'name',
            'icon',
            'link',
            'username_or_id',
        )



class GlobalSettingSerializers(serializers.ModelSerializer):
    """Get site global settings."""

    socials = serializers.SerializerMethodField()

    class Meta:
        model = SiteGlobalSetting
        fields = ('name', 'logo', 'favicon', 'slogan', 'copyright', 'phone', 'fax', 'email', 'address', 'map',
                  'longitude', 'latitude', 'zoom', 'socials',)

    @extend_schema_field(SocialMediaSerializers)
    def get_socials(self, obj):
        return SocialMediaSerializers(instance=SocialMediaSetting.objects.all(), many=True, read_only=True,
                                      context=self.context).data
