from django.conf import settings
from importlib import import_module


def get_product_variant_model():
    """
    Returns the product model that is used by this cart.
    """
    package, module = settings.CART_PRODUCT_VARIANT_MODEL.rsplit('.', 1)
    return getattr(import_module(package), module)
