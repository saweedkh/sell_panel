# Django Built-in modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.utils import timezone

# Local apps
from area.models import City, Province
from utils.models import AbstractDateTimeModel, AbstractUUIDModel
from .managers import UserManager
from django.conf import settings

# Python Standard Library
import uuid as _uuid

# Third Party Packages
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from smart_selects.db_fields import ChainedForeignKey


class User(AbstractBaseUser, AbstractDateTimeModel, AbstractUUIDModel, PermissionsMixin):
    """
    This models inherits from django base user.
    """

    uuid = models.UUIDField(unique=True, default=_uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('نام کاربری'),
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name=_('نام و نام خانوادگی'),
    )
    mobile_number = PhoneNumberField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_('شماره موبایل'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    birthday = models.DateField(
        _("تاریخ تولد"),
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to='users/avatar/%y/%m/%d',
        null=True,
        blank=True,
        verbose_name=_('تصویر پروفایل'),
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(250, 250)],
        format='PNG',
        options={'quality': 70}
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_('ادمین'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('کارمند'),
    )

    address = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('آدرس')
    )
    
    confirm_profile = models.BooleanField(
        _("تایید پروفایل"),
        default=False,
    )
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('full_name',)
    objects = UserManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        return self.full_name

    @property
    def fullname(self):
        return f'{self.full_name}'
    
    def get_full_name(self):
        return self.fullname


    def get_avatar(self):
        try:
            if self.avatar.url and self.avatar_thumbnail.url and self.avatar.file:
                image = self.avatar_thumbnail.url
        except:
            image = settings.DEFAULT_AVATAR_PATH
        return image

    def is_admin(self):
        return self.is_authenticated and self.is_superuser and self.is_staff


    
    def get_profile_completion_percentage(self):
        user_fields = [
            self.full_name,
            self.mobile_number,
            self.birthday,
            self.email,
            self.avatar,
        ]

        filled_user_fields = sum(1 for field in user_fields if field)
        
        total_user_fields = len(user_fields)
        
        
        total_fields = total_user_fields 
        filled_fields = filled_user_fields 
        
        
        if total_fields > 0:
            completion_percentage = (filled_fields / total_fields) * 100
        else:
            completion_percentage = 100  
        
        return round(completion_percentage)



    

class UserAddress(AbstractDateTimeModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("کاربر"),
        related_name='addresses',
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("نام محل"),
        null=True,
        blank=True
    )
    address = models.TextField(
        verbose_name=_("آدرس"),
        null=True,
        blank=True
    )
    mobile_number = PhoneNumberField(
        verbose_name=_("شماره تلفن"),
        max_length=255,
        null=True,
        blank=True
    )
    postal_code = models.PositiveBigIntegerField(
        verbose_name=_("کدپستی"),
        null=True,
        blank=True
    )
    is_default = models.BooleanField(
        verbose_name=_("پیشفرض برای این ادرس ارسال شود"),
        default=False,
    )

    class Meta:
        verbose_name = _("آدرس")
        verbose_name_plural = _("آدرس ها")
        ordering = ('-created',)

    def __str__(self):
        return f"{self.author} - {self.name}"


class MobilePhoneVerify(AbstractDateTimeModel):
    USABLE = 0
    USELESS = 1
    STATUS_CHOICE = (
        (USABLE, _('قابل استفاده')),
        (USELESS, _('غیر قابل استفاده')),
    )
    mobile_number = PhoneNumberField(
        unique=True,
        verbose_name=_('شماره موبایل'),
    )
    code = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('کد'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICE,
        default=USABLE,
        verbose_name=_('وضعیت'),
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('کد تایید')
        verbose_name_plural = _('کد های تایید')

    def __str__(self):
        return str(self.mobile_number)

    