from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FaqsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faqs'
    verbose_name = _('سوالات متداول و قوانین')
