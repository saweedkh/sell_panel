# Local Apps
from .models import AbstractBaseSeoModel, AbstractContentModel, AbstractDateTimeModel

# Third Party Packages
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes


class BaseDateTimeModelSerializer(serializers.ModelSerializer):
    """Get DateTime ."""
    jcreated = serializers.SerializerMethodField()
    jupdated = serializers.SerializerMethodField()

    class Meta:
        model = AbstractDateTimeModel
        fields = ('created', 'jcreated', 'updated', 'jupdated',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_jcreated(self, obj):
        return obj.jcreated()

    @extend_schema_field(OpenApiTypes.STR)
    def get_jupdated(self, obj):
        return obj.jupdated()


class BaseSeoSerializer(serializers.ModelSerializer):
    """Get Seo items ."""
    page_title = serializers.SerializerMethodField()
    page_description = serializers.SerializerMethodField()
    page_keywords = serializers.SerializerMethodField()
    meta_tags = serializers.SerializerMethodField()

    class Meta:
        model = AbstractBaseSeoModel
        fields = ('slug', 'page_display_status', 'page_title', 'page_description',
                  'page_keywords', 'canonical_link', 'meta_tags',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_page_title(self, obj):
        return obj.page_title

    @extend_schema_field(OpenApiTypes.STR)
    def get_page_description(self, obj):
        return obj.page_description

    @extend_schema_field(OpenApiTypes.STR)
    def get_page_keywords(self, obj):
        return obj.page_keywords

    @extend_schema_field(OpenApiTypes.STR)
    def get_meta_tags(self, obj):
        return obj.meta_tags()


class BaseContentSerializer(serializers.ModelSerializer):
    """Get Content items ."""

    class Meta:
        model = AbstractContentModel
        fields = ('description', 'content',)
