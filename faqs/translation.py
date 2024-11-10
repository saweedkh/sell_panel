from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Category as FAQCategory,
    FAQItems,
    TermsCategory,
    TermsItems
)


class FAQCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


class FAQItemsTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)


class TermsCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


class TermsItemsTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(FAQCategory, FAQCategoryTranslationOptions, )
translator.register(FAQItems, FAQItemsTranslationOptions, )
translator.register(TermsCategory, TermsCategoryTranslationOptions, )
translator.register(TermsItems, TermsItemsTranslationOptions, )
