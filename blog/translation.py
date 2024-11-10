# Local Apps
from .models import AbstractBlogCategory, AbstractBlogPost
from seo.translation import (
    AbstractBaseSeoModelTranslationOptions,
    AbstractContentModelTranslationOptions,
)

# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


#
class AbstractBlogCategoryTranslationOptions(TranslationOptions):
    fields = (
        'name', 'image',
        *AbstractContentModelTranslationOptions.fields,
        *AbstractBaseSeoModelTranslationOptions.fields,
    )
    fallback_values = {
        'name': '---',
        'image': None,
    }


#
class AbstractBlogPostTranslationOptions(TranslationOptions):
    fields = (
        'name', 'image',
        *AbstractContentModelTranslationOptions.fields,
        *AbstractBaseSeoModelTranslationOptions.fields,
    )
    fallback_values = {
        'name': '---',
        'image': None,
    }

class AbstractBlogTagTranslationOptions(TranslationOptions):
    fields = (
        'name',
        *AbstractBaseSeoModelTranslationOptions.fields
    )

# # translator.register(AbstractBlogCategory, AbstractBlogCategoryTranslationOptions, )
# # translator.register(AbstractBlogPost, AbstractBlogPostTranslationOptions, )
