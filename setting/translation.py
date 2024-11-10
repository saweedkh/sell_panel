# Local Apps
from .models import (
    SiteGlobalSetting,
    SocialMediaSetting,
)

# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


class SiteGlobalSettingTranslationOptions(TranslationOptions):
    fields = ('name', 'slogan', 'copyright', 'phone', 'address', 'map',)


class SocialMediaSettingTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(SiteGlobalSetting, SiteGlobalSettingTranslationOptions, )
translator.register(SocialMediaSetting, SocialMediaSettingTranslationOptions, )
