# Django Built-in Modules
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-party Apps
from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)

# local apps
from utils.models import AbstractDateTimeModel


class MenuObject(MPTTModel, AbstractDateTimeModel):
    name = models.CharField(
        max_length=50,
        verbose_name=_('نام')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('والد')
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('لینک'),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('نوع محتوا')
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('شی مرتبط')
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    class MPTTMeta:
        order_insertion_by = ('created',)

    class Meta:
        verbose_name = _('منو')
        verbose_name_plural = _('منوها')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.get_link

    @property
    def get_link(self):
        if self.url:
            return self.url
        elif self.content_object:
            return self.content_object.get_absolute_url()
        return '#'
