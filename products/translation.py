# Local Apps

from products.models import Product
from seo.translation import AbstractBaseSeoModelTranslationOptions
from utils.translation import AbstractStaticPageTranslationOptions

# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions


class ProductTranslationOptions(TranslationOptions):
    fields = (
        *AbstractBaseSeoModelTranslationOptions.fields,
    )


translator.register(Product, ProductTranslationOptions, )
