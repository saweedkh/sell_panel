# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel



class Province(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('نام'),
    )

    class Meta:
        verbose_name = _('استان')
        verbose_name_plural = _('استان ها')

    def __str__(self):
        return self.name


class City(AbstractDateTimeModel):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_('استان'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )

    class Meta:
        unique_together = ('province', 'name',)
        verbose_name = _('شهر')
        verbose_name_plural = _('شهر ها')

    def __str__(self):
        return self.name
