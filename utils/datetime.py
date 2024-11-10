# Django Built-in modules
from django.conf import settings
from django.utils.timezone import make_aware


def check_and_make_aware(datetime_instance):
    if settings.USE_TZ:
        return make_aware(datetime_instance)
    return datetime_instance
