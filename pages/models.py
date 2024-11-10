# Django Built-in modules
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

# Local apps
from utils.models import AbstractDateTimeModel, AbstractStaticPage
from seo.models import AbstractBaseSeoModel

# Third Party Packages
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Home(AbstractStaticPage, AbstractBaseSeoModel, AbstractDateTimeModel):
    video = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ویدیو صفحه اصلی'),
        help_text=_('کد امبد آپارات یا یوتیوب'),
    )

    class Meta:
        verbose_name = _('صفحه اصلی')
        verbose_name_plural = _('صفحه اصلی')

    def __str__(self):
        return str(_('صفحه اصلی'))

    @staticmethod
    def get_absolute_url():
        return reverse('pages:home')

    @property
    def default_search_engine_title(self):
        return self.__str__()

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def get_manager_image(self):
        try:
            if self.about_us_image.url and self.about_us_image_thumbnail.url and self.about_us_image.file:
                image = self.about_us_image_thumbnail.url
        except:
            image = static('defaults/default.png')
        return image


class About(AbstractStaticPage, AbstractBaseSeoModel, AbstractDateTimeModel):
    video = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('ویدیو صفحه درباره ما'),
        help_text=_('کد امبد آپارات یا یوتیوب'),
    )

    class Meta:
        verbose_name = _('درباره')
        verbose_name_plural = _("درباره")

    def __str__(self):
        return str(_('درباره'))

    @staticmethod
    def get_absolute_url():
        return reverse('pages:about_us')

    @property
    def default_search_engine_title(self):
        return self.__str__()

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

