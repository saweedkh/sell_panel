# Local Apps
from .models import MetadataModel

# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


class AbstractBaseSeoModelTranslationOptions(TranslationOptions):
    fields = ('slug', 'search_engine_title', 'search_engine_description', 'search_engine_keywords', 'canonical_link',)


class AbstractContentModelTranslationOptions(TranslationOptions):
    fields = ('description', 'content',)


class MetadataModelTranslationOptions(TranslationOptions):
    fields = ('value',)


translator.register(MetadataModel, MetadataModelTranslationOptions, )
