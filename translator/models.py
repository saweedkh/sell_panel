# Django Build-in
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel


class TranslationQuerySet(models.QuerySet):
    def get_default(self):
        if self.first():
            return self.first()
        else:
            return self.create()

    def is_active(self):
        if self.get_default().active:
            return True


class TranslatorSetting(AbstractDateTimeModel):
    CHAT_GPT = 0
    GOOGLE = 1
    MICROSOFT = 2

    ENGINES = (
        (GOOGLE, _('GoogleTranslator')),
    )
    source_language = models.CharField(
        max_length=200,
        verbose_name=_('زبان مبدا'),
        default=settings.LANGUAGE_CODE,
        choices=settings.LANGUAGES,
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("فعال"),
        help_text=_('بعد از تغییر لطفا پروژه را ری استارت کنید')
    )
    search_engine = models.PositiveSmallIntegerField(
        choices=ENGINES,
        default=GOOGLE,
        verbose_name=_("موتور ترجمه")
    )
    objects = TranslationQuerySet.as_manager()

    class Meta:
        verbose_name = _('تنظیمات مترجم')
        verbose_name_plural = _('تنظیمات مترجم')

    def __str__(self):
        return str('تنظیمات مترجم')
