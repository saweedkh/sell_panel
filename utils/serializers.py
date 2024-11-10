# Local Apps
from .models import AbstractStaticPage
from .mixins import SerializerTranslationMixin

# Third Party Packages
from rest_framework import serializers


class BaseStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractStaticPage
        fields = ('content',)


class CustomModelSerializers(SerializerTranslationMixin, serializers.ModelSerializer):
    pass

class TranslationModelSerializers(SerializerTranslationMixin, serializers.ModelSerializer):
    pass
