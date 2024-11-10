# Local Apps
from .models import (
    Category as FAQCategory,
    FAQItems,
    TermsCategory,
    TermsItems
)
from .translation import (
    FAQCategoryTranslationOptions,
    FAQItemsTranslationOptions,
    TermsCategoryTranslationOptions,
    TermsItemsTranslationOptions,
)
from utils.serializers import TranslationModelSerializers

# Third Party Packages
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class FAQListSerializer(TranslationModelSerializers):
    """Get all faqs."""

    class Meta:
        model = FAQItems
        fields = ('pk', 'category', 'question', 'answer',)
        model_translation = FAQItemsTranslationOptions


class FAQCategoryListSerializer(TranslationModelSerializers):
    """Get all faqs categories."""

    faqs = serializers.SerializerMethodField()

    class Meta:
        model = FAQCategory
        fields = ('pk', 'name', 'description', 'faqs')
        model_translation = FAQCategoryTranslationOptions

    @extend_schema_field(FAQListSerializer)
    def get_faqs(self, obj):
        return FAQListSerializer(instance=FAQItems.objects.filter(category=obj, display=True), many=True,
                                 read_only=True, context=self.context).data


class TermsItemsListSerializer(TranslationModelSerializers):
    """Get all terms."""

    class Meta:
        model = TermsItems
        fields = ('pk', 'category', 'name', 'description',)
        model_translation = TermsItemsTranslationOptions


class TermsCategoryListSerializer(TranslationModelSerializers):
    """Get all terms categories."""

    terms = serializers.SerializerMethodField()

    class Meta:
        model = TermsCategory
        fields = ('pk', 'name', 'description', 'terms',)
        model_translation = TermsCategoryTranslationOptions

    @extend_schema_field(TermsItemsListSerializer)
    def get_terms(self, obj):
        return TermsItemsListSerializer(instance=TermsItems.objects.filter(category=obj, display=True), many=True,
                                        read_only=True, context=self.context).data
