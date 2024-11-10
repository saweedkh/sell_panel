# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


class AbstractStaticPageTranslationOptions(TranslationOptions):
    fields = ('content',)
