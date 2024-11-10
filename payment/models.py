# Django Built-in modules
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel, AbstractUUIDModel, AbstractStaticPage

# Third Party Packages
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Receipt(AbstractDateTimeModel):
    AWAITING_CHECK = 1
    ACCEPTED = 2
    REJECTED = 3

    RECEIPT_STATUS_CHOICES = (
        (AWAITING_CHECK, 'در انتظار بررسی'),
        (ACCEPTED, 'تایید شده'),
        (REJECTED, 'رد شده'),
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        verbose_name=_('سفارش'),
    )
    amount = models.PositiveBigIntegerField(
        verbose_name=_('مبلغ'),
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='bank-receipts/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 840)],
        format='JPEG',
        options={'quality': 90}
    )
    tracking_code = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('کد رهگیری بانکی'),
    )
    status = models.PositiveSmallIntegerField(
        choices=RECEIPT_STATUS_CHOICES,
        default=AWAITING_CHECK,
        verbose_name=_('وضعیت'),
    )

    class Meta:
        verbose_name = _('رسید')
        verbose_name_plural = _('رسید ها')
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class PaymentSettingQueryset(models.QuerySet):

    def get_first(self):
        if not self.exists():
            first = self.create()
        else:
            first = self.first()
        return first


class PaymentSetting(AbstractDateTimeModel):
    enable_gateway = models.BooleanField(
        default=True,
        verbose_name=_('درگاه بانکی فعال باشد'),
    )
    enable_transfer = models.BooleanField(
        default=False,
        verbose_name=_('پرداخت کارت به کارت فعال باشد'),
    )
    enable_wallet = models.BooleanField(
        default=True,
        verbose_name=_('کیف پول فعال باشد'),
    )
    enable_post_paid = models.BooleanField(
        default=False,
        verbose_name=_('پرداخت در محل فعال باشد'),
    )
    prepayment_status_for_post_paid = models.BooleanField(
        default=False,
        verbose_name=_('پرداخت بیعانه برای روش پرداخت در محل'),
    )
    prepayment_percentage = models.PositiveSmallIntegerField(
        default=30,
        verbose_name=_('درصد بیعانه'),
        help_text=_('۱ تا ۱۰۰ (درصد بیعانه از جمع کل سفارش کسر می شود.)'),
    )
    transfer_content = RichTextUploadingField(
        blank=True,
        verbose_name=_('توضیحات'),
    )

    objects = PaymentSettingQueryset.as_manager()

    class Meta:
        verbose_name = _('پیکربندی پرداخت')
        verbose_name_plural = _("پیکربندی پرداخت")

    def __str__(self):
        return str(_('پیکربندی پرداخت'))

    def payment_status(self, user_is_authenticated):
        # Hard coded
        payment_method_choices = apps.get_model(app_label='orders', model_name='order').PAYMENT_METHOD_CHOICES
        payment_statuses = (
            (payment_method_choices[0], all([self.enable_gateway])),
            (payment_method_choices[1], all([self.enable_wallet, user_is_authenticated])),
            (payment_method_choices[2], all([self.enable_transfer])),
            (payment_method_choices[3], all([self.enable_post_paid])),
        )

        filtered_payment_methods = tuple(
            payment_status[0] for payment_status in payment_statuses
            if payment_status[1]
        )
        return filtered_payment_methods


class CardQueryset(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def has_active(self):
        if not self.exists():
            return self.none()

        if self.active().count() < 1:
            last = self.last()
            last.active = True
            last.save()
        return self


class Card(AbstractDateTimeModel):
    payment_setting = models.ForeignKey(
        PaymentSetting,
        on_delete=models.CASCADE,
        verbose_name=_('پیکربندی'),
    )
    fullname = models.CharField(
        max_length=200,
        verbose_name=_('نام صاحب حساب'),
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name=_('نام بانک'),
    )
    bank_logo = models.ImageField(
        null=True,
        blank=True,
        upload_to='bank-logo/',
        verbose_name=_('لوگوی بانک'),
    )
    bank_logo_thumbnail = ImageSpecField(
        source='bank_logo',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 70}
    )
    card_number = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        verbose_name=_('شماره کارت'),
    )
    shaba = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('شماره شبا'),
    )
    account_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('شماره حساب'),
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_('فعال'),
    )

    objects = CardQueryset.as_manager()

    class Meta:
        verbose_name = _('کارت بانکی')
        verbose_name_plural = _('کارت های بانکی')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.bank_name} - {self.fullname}'

    def get_bank_logo(self):
        if self.bank_logo and self.bank_logo_thumbnail.file:
            return self.bank_logo_thumbnail.url

    def pretty_card_number(self):
        card_number = self.card_number
        try:
            pretty = ' '.join([card_number[i:i + 4] for i in range(0, len(card_number), 4)])
            return pretty
        except Exception:
            return card_number
