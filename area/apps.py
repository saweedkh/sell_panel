from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AreaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'area'
    verbose_name = _('مناطق')
