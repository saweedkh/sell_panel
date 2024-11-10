# Local Apps
from .models import (
    Home,
    About,
)
from seo.translation import AbstractBaseSeoModelTranslationOptions
from utils.translation import AbstractStaticPageTranslationOptions

# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


class HomeTranslationOptions(TranslationOptions):
    fields = (
        *AbstractStaticPageTranslationOptions.fields,
        *AbstractBaseSeoModelTranslationOptions.fields,
    )


class AboutTranslationOptions(TranslationOptions):
    fields = (
        *AbstractStaticPageTranslationOptions.fields,
        *AbstractBaseSeoModelTranslationOptions.fields,
    )


translator.register(Home, HomeTranslationOptions, )
translator.register(About, AboutTranslationOptions, )

