# Local Apps
from .models import (
    Province,
    City,
)
from seo.translation import AbstractBaseSeoModelTranslationOptions

# Third Party Packages
from modeltranslation.translator import register, TranslationOptions


@register(Province)
class ProvinceTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)
