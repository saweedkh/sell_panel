# Django Built-in modules
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from .jdatetime import standard_jalali_datetime_format

# Python Standard Library
from uuid import uuid4

# Third Party Packages
from ckeditor_uploader.fields import RichTextUploadingField


# Models

class AbstractUUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ایجاد شده'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('آپدیت شده'),
    )

    class Meta:
        abstract = True

    @admin.display(description=_('ایجاد شده'), empty_value='-')
    def jcreated(self):
        return standard_jalali_datetime_format(self.created)

    jcreated.admin_order_field = 'created'

    @admin.display(description=_('آپدیت شده'), empty_value='-')
    def jupdated(self):
        return standard_jalali_datetime_format(self.updated)

    jupdated.admin_order_field = 'updated'


class AbstractStaticPage(models.Model):
    content = RichTextUploadingField(
        blank=True,
        verbose_name=_('محتوا'),
    )

    class Meta:
        abstract = True
