# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from phonenumber_field.modelfields import PhoneNumberField


class ContactUsMessages(AbstractDateTimeModel):
    MESSAGE = 1
    SUGGESTIONS = 2
    TYPE_CHOICES = (
        (MESSAGE, _('فرم تماس')),
        (SUGGESTIONS, _('پیشنهادات')),
    )
    type = models.SmallIntegerField(
        choices=TYPE_CHOICES,
        verbose_name=_('نوع'),
    )
    fullname = models.CharField(
        max_length=50,
        verbose_name=_('نام و نام خانوادگی'),
    )
    phone = PhoneNumberField(
        max_length=50,
        verbose_name=_('شماره موبایل'),
    )
    email = models.EmailField(
        verbose_name=_('ایمیل'),
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=_('موضوع'),
    )
    message = models.TextField(
        verbose_name=_('متن پیام'),
    )
    is_checked = models.BooleanField(
        default=False,
        verbose_name=_('بررسی شده؟'),
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('پیام')
        verbose_name_plural = _("پیام ها")

    def __str__(self):
        return self.fullname
