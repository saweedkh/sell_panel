# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from ckeditor_uploader.fields import RichTextUploadingField


class Category(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('توضیحات'),
    )
    display = models.BooleanField(
        default=True,
        verbose_name=_('نمایش'),
    )

    class Meta:
        verbose_name = _('دسته بندی سوالات متداول')
        verbose_name_plural = _("دسته بندی های سوالات متداول")

    def __str__(self):
        return self.name


class FAQItems(AbstractDateTimeModel):
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('دسته بندی'),
    )
    question = models.TextField(
        verbose_name=_('سوال')
    )
    answer = RichTextUploadingField(
        verbose_name=_('پاسخ')
    )
    display = models.BooleanField(
        default=True,
        verbose_name=_('نمایش'),
    )

    class Meta:
        verbose_name = _('پرسش')
        verbose_name_plural = _("پرسش ها")

    def __str__(self):
        return self.question


class TermsCategory(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('توضیحات'),
    )
    display = models.BooleanField(
        default=True,
        verbose_name=_('نمایش'),
    )

    class Meta:
        verbose_name = _('دسته بندی قوانین و مقررات')
        verbose_name_plural = _("دسته بندی های قوانین و مقررات")

    def __str__(self):
        return self.name


class TermsItems(AbstractDateTimeModel):
    category = models.ForeignKey(
        TermsCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('دسته بندی'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    description = RichTextUploadingField(
        verbose_name=_('توضیحات')
    )
    display = models.BooleanField(
        default=True,
        verbose_name=_('نمایش'),
    )

    class Meta:
        verbose_name = _('قانون')
        verbose_name_plural = _("قوانین")

    def __str__(self):
        return self.name
