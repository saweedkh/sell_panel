from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'setting'
    verbose_name = _('تنظیمات')
