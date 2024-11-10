# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class SiteGlobalSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام وبسایت'),
    )
    slogan = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('شعار'),
    )
    copyright = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('متن کپی رایت'),
    )
    logo = models.ImageField(
        upload_to='site/',
        null=True,
        blank=True,
        verbose_name=_('لوگو'),
    )
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(250, 250)],
        format='PNG',
        options={'quality': 80}
    )
    favicon = models.ImageField(
        upload_to='site/',
        null=True,
        blank=True,
        verbose_name=_('فاوآیکون'),
    )
    favicon_thumbnail = ImageSpecField(
        source='favicon',
        processors=[ResizeToFill(180, 180)],
        format='PNG',
        options={'quality': 80}
    )
    phone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('شماره تلفن'),
    )
    fax = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('فکس'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('آدرس'),
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('نقشه'),
        help_text=_('کد embed گوگل مپ'),
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('طول جغرافیایی'),
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('عرض جغرافیایی'),
    )
    zoom = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('بزرگنمایی'),
    )

    class Meta:
        verbose_name = _('پیکربندی سایت')
        verbose_name_plural = _("پیکربندی سایت")

    def __str__(self):
        return str(_('پیکربندی سایت'))

    @classmethod
    def get_default_setting(cls):
        obj = cls.objects.last()
        if not obj:
            obj = cls.objects.create(name='Saweed')
        return obj

    @property
    def default_search_engine_title(self):
        return self.__str__()

    @property
    def get_logo(self):
        if self.logo and self.logo.file:
            return self.logo_thumbnail.url

    @property
    def get_favicon(self):
        if self.favicon and self.favicon.file:
            return self.favicon_thumbnail.url

    def have_contact_ways(self):
        return self.phone or self.email


class SocialMediaSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_('نام'),
    )
    username_or_id = models.CharField(
        max_length=100,
        verbose_name=_('نام کاربری یا آیدی'),
        help_text=_('مثال: firefly@'),
    )
    icon = models.ImageField(
        verbose_name=_('آیکون'),
        upload_to='site/socials/'
    )
    link = models.URLField(
        verbose_name=_('لینک'),
    )

    class Meta:
        verbose_name = _('شبکه اجتماعی')
        verbose_name_plural = _("شبکه های اجتماعی")

    def __str__(self):
        return self.name
