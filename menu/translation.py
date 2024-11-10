from modeltranslation.translator import translator, TranslationOptions
from .models import MenuObject


class MenuObjectTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(MenuObject, MenuObjectTranslationOptions, )
