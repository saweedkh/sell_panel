# Django Build-in
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel


class Member(AbstractDateTimeModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('ایمیل'),
    )

    class Meta:
        verbose_name = _("عضو")
        verbose_name_plural = _("اعضا")
        ordering = ('-created',)

    def __str__(self):
        return self.email
