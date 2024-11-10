# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from mptt.models import MPTTModel

from django.conf import settings

# Third Party Packages
from mptt.fields import TreeForeignKey


class BaseCommentModelQueryset(models.QuerySet):
    def accepted(self):
        return self.filter(status=AbstractBaseComment.ACCEPT)


class AbstractBaseComment(MPTTModel, models.Model):
    IN_QUEUE = 0
    ACCEPT = 1
    DECLINE = 2
    STATUS_CHOICE = (
        (IN_QUEUE, _('در صف')),
        (ACCEPT,  _('پذیرش')),
        (DECLINE,  _('رد')),
    )
    COMMENT = 0
    QA = 1
    TYPE_CHOICE = (
        (COMMENT, _('نظر')),
        (QA, _('پرسش و پاسخ'))
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('والد'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('کاربر'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    review = models.TextField(
        max_length=400,
        verbose_name=_('متن دیدگاه'),
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICE,
        default=IN_QUEUE,
        verbose_name=_('وضعیت'),
    )
    comment_type = models.SmallIntegerField(
        choices=TYPE_CHOICE,
        default=COMMENT,
        verbose_name=_('نوع'),
    )

    accepted = BaseCommentModelQueryset.as_manager()  # custom manager for accepted comments

    class MPTTMeta:
        order_insertion_by = ('created',)
        unique_together = ('name', 'parent',)

    class Meta:
        abstract = True

    @property
    def is_admin_comment(self):
        if self.user:
            if self.user.is_staff and self.user.is_superuser:
                return True
        return False
