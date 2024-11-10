# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from mptt.models import MPTTModel, TreeForeignKey


class AbstractBaseCategory(MPTTModel, AbstractDateTimeModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('والد'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )

    class MPTTMeta:
        order_insertion_by = ('created',)
        unique_together = ('name', 'parent',)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
