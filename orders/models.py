# Django Built-in modules
from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericRelation
from django.http import Http404
from django.shortcuts import reverse, render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib import admin

# Local apps
from utils.models import AbstractDateTimeModel, AbstractUUIDModel
from account.models import (
    User,
    UserAddress,
)
from products.models import (
    Product,
    Category,
    Variant,
    AttributeValue,
)
from products.mixins import ModelDiffMixin
from area.models import (
    Province,
    City,
)
from coupon.models import DiscountCoupon
from gateways.utils import (
    generate_tracking_code,
    generate_reference_code,
)
from payment.models import PaymentSetting
from utils.jdatetime import standard_jalali_datetime_format

# Third Party Packages
from phonenumber_field.modelfields import PhoneNumberField
from gateways import bankfactories, models as bank_models
from gateways.exceptions import BankGatewaysException


class Order(ModelDiffMixin, AbstractDateTimeModel, AbstractUUIDModel):
    FROM_WEBSITE = 1
    FROM_SOCIAL_MEDIA = 2
    FROM_STORE = 3

    ORDER_THROUGH_CHOICES = (
        (FROM_WEBSITE, _('سایت')),
        (FROM_SOCIAL_MEDIA, _('شبکه های اجتماعی')),
        (FROM_STORE, _('فروشگاه')),
    )

    AWAITING_PAYMENT = 1
    AWAITING_CHECK = 2
    DOING = 3
    PACKING = 4
    DONE = 5
    SENT = 6
    SURVEY = 7
    CANCELED = 8
    RETURNED = 9

    ORDER_STATUS_CHOICES = (
        (AWAITING_PAYMENT, _('در انتظار پرداخت')),
        (AWAITING_CHECK, _('در انتظار بررسی')),
        (DOING, _('در حال انجام')),
        (PACKING, _('بسته بندی')),
        (SENT, _('ارسال شده')),
        (DONE, _('تکمیل شده')),
        (CANCELED, _('لغو شده')),
        (RETURNED, _('مسترد شده')),
    )

    BANK_GATEWAY = 1
    WALLET = 2
    TRANSFER = 3
    POST_PAID = 4
    POS = 5
    CASH = 6
    PAYMENT_METHOD_CHOICES = (
        (BANK_GATEWAY, 'درگاه بانکی'),
        (WALLET, 'کیف پول'),
        (TRANSFER, 'کارت به کارت'),
        (POST_PAID, 'پرداخت در محل'),
        (POS, 'دستگاه پوز'),
        (CASH, 'نقدی'),
    )

    WAREHOUSE_DECREASE = -1
    WAREHOUSE_NO_CHANGE = 0
    WAREHOUSE_INCREASE = 1
    WAREHOUSE_FORBIDDEN = None

    tracking_code = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
        default=generate_tracking_code,
        verbose_name=_('شماره پیگیری'),
    )
    reference_code = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
        default=generate_reference_code,
        verbose_name=_('کد ارجاع'),
    )
    postal_tracking_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('کد رهگیری پستی'),
    )
    through = models.PositiveSmallIntegerField(
        choices=ORDER_THROUGH_CHOICES,
        default=FROM_WEBSITE,
        verbose_name=_('از طریق'),
    )
    registrar = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='registrar_set',
        null=True,
        blank=True,
        verbose_name=_('فروشنده'),
    )

    order_status = models.PositiveSmallIntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=AWAITING_PAYMENT,
        verbose_name=_('وضعیت سفارش'),
    )
    send_notification_sms = models.BooleanField(
        default=True,
        verbose_name=_('ارسال پیامک اطلاع رسانی')
    )
    mark_order = models.BooleanField(
        default=False,
        verbose_name=_('نشان کردن'),
        help_text=_('سفارش را برای موارد خاص مثل تاخیر در بسته بندی، مشکل در پرداخت یا... علامت گذاری کنید.'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('مشتری'),
    )

    transaction = GenericRelation(bank_models.Bank)

    first_name = models.CharField(
        max_length=200,
        verbose_name=_('نام'),
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('نام خانوادگی'),
    )
    mobile_number = PhoneNumberField(
        max_length=50,
        verbose_name=_('شماره موبایل'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    province_id = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('استان')
    )
    province = models.CharField(
        max_length=200,
        verbose_name=_('استان')
    )
    city_id = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('شهر')
    )
    city = models.CharField(
        max_length=200,
        verbose_name=_('شهر')
    )
    address_id = models.ForeignKey(
        UserAddress,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('آدرس'),
    )
    address = models.TextField(
        verbose_name=_('آدرس'),
    )
    postal_code = models.CharField(
        null=True,
        blank=True,
        verbose_name=_('کد پستی'),
        max_length=20,
    )
    note = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('یادداشت'),
    )

    packing_type = models.ForeignKey(
        'PackingType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('بسته بندی'),
    )
    discount_code = models.ForeignKey(
        DiscountCoupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('کوپن تخفیف'),
    )
    commodity_prices = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('قیمت کالاها'),
    )
    total_discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('تخفیف'),
    )
    discount_amount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('مبلغ کوپن تخفیف'),
    )
    prepayment = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('بیعانه'),
    )
    payable = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('قابل پرداخت'),
    )
    payment_method = models.PositiveSmallIntegerField(
        choices=PAYMENT_METHOD_CHOICES,
        default=BANK_GATEWAY,
        verbose_name=_('روش پرداخت'),
    )
    paid = models.BooleanField(
        default=False,
        verbose_name=_('پرداخت شده'),
    )
    deposit_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاریخ واریز'),
    )
    user_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP'),
    )
    user_agent = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('User Agent')
    )
    register_in_accounting_system = models.BooleanField(
        default=False,
        verbose_name=_('ثبت در سیستم حسابداری'),
    )

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارشات')
        ordering = ('-created',)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__last_order_status__ = None

    def __str__(self):
        return str(self.tracking_code)

    def get_absolute_url(self):
        return reverse('account:order_detail', args=[self.tracking_code])

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def complete_address(self):
        return f'{self.province}، {self.city}، {self.address}'

    @property
    def payment_order_link(self):
        # return 'https://' + settings.SITE_DOMAIN + reverse('orders:order_review', args=[self.uuid])
        return reverse('orders:order_review', args=[self.uuid])
        # return ''

    def create_invoice_absolute_url(self):
        return reverse('orders:create_invoice', args=[self.id])

    def last_invoice_absolute_url(self):
        invoice = self.invoice_set.last()
        if invoice is None:
            return None
        return reverse('orders:invoice', args=[invoice.id])

    @property
    def is_payable(self):
        if (self.order_status == self.AWAITING_PAYMENT or self.order_status == self.AWAITING_CHECK) and not self.paid:
            return True
        return False

    @property
    def get_payable_in_post_paid(self):
        if self.payment_method == self.POST_PAID:
            prepayment = self.prepayment or 0
            amount = self.payable - prepayment
            return amount
        else:
            return self.payable

    @classmethod
    def create(cls, user, order_form_cleaned_data, cart):
        if user.is_authenticated:
            address = order_form_cleaned_data.get('address_id')
            order = cls.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                mobile_number=address.mobile_number if address.mobile_number else user.mobile_number,
                email=user.email,
                province_id=address.province,
                city_id=address.city,
                address_id=address,
                address=address.complete_address,
                postal_code=address.postal_code,
                note=order_form_cleaned_data.get('note'),
                discount_code_id=cart.discount.get('pk') if cart.discount else None,
                payment_method=order_form_cleaned_data.get('payment_method'),
            )
        else:
            order = cls.objects.create(
                first_name=order_form_cleaned_data.get('first_name'),
                last_name=order_form_cleaned_data.get('last_name'),
                mobile_number=order_form_cleaned_data.get('mobile_number'),
                email=order_form_cleaned_data.get('email'),
                province_id=order_form_cleaned_data.get('province_id'),
                city_id=order_form_cleaned_data.get('city_id'),
                address=order_form_cleaned_data.get('address'),
                postal_code=order_form_cleaned_data.get('postal_code'),
                note=order_form_cleaned_data.get('note'),
                discount_code_id=cart.discount.get('pk') if cart.discount else None,
                payment_method=order_form_cleaned_data.get('payment_method'),
            )
        OrderItem.create(order_id=order.pk, variant_items=cart.items)
        order.save()
        return order

    @classmethod
    def calculate_prices(cls, instance):
        commodity_prices = 0
        total_discount = 0
        payable = 0
        order_items = instance.orderitem_set.all()
        for order_item in order_items:
            commodity_prices += order_item.get_total_price
            total_discount += order_item.get_total_discount
            payable += order_item.amount_payable

        instance.commodity_prices = commodity_prices
        instance.total_discount = total_discount
        
        discount_code = instance.discount_code
        instance.payable = payable
        if discount_code:
            instance.discount_amount = discount_code.calculate_discount(payable)
            final_price = payable - instance.discount_amount
            instance.payable = 0 if final_price < 0 else final_price
        elif instance.discount_amount:
            final_price = payable + instance.discount_amount
            instance.payable = 0 if final_price < 0 else final_price
            instance.discount_amount = None


    @classmethod
    def set_province_and_city_in_every_change(cls, instance):
        province_id = instance.province_id
        if province_id:
            instance.province = province_id.name

        city_id = instance.city_id
        if city_id:
            instance.city = city_id.name

    def choose_payment_method(self, request):
        payment_method = int(self.payment_method)
        if payment_method == self.BANK_GATEWAY:
            # SendSMSWithPattern(
            #     str(self.mobile_number.national_number),
            #     {'fname': self.first_name, 'lname': self.last_name, },
            # ).send()
            return self.go_to_gateway(request)
        elif payment_method == self.TRANSFER:
            return redirect('payment:upload_bank_receipt', self.tracking_code)
        elif payment_method == self.POST_PAID:
            return redirect('payment:post_paid_payment', self.tracking_code)
        elif payment_method == self.WALLET:
            return redirect('payment:withdraw_from_wallet', self.tracking_code)
        else:
            return self.go_to_gateway(request)

    def payment(self, request):
            return self.go_to_gateway(request)

    def go_to_gateway(self, request):
        try:
            factory = bankfactories.BankFactory()
            bank = factory.auto_create()
            bank.set_user_id(self.user)
            bank.set_request(request)
            bank.set_amount(self.payable)
            bank.set_content_type(ContentType.objects.get_for_model(self))
            bank.set_object_id(self.pk)
            bank.set_client_callback_url(reverse('payment:get_invoice'))
            bank.set_mobile_number(self.mobile_number)
            self.transactions = bank.ready()
            self.tracking_code = bank.get_tracking_code()
            self.save()
            
            url = bank.redirect_gateway()
            return url
        except Exception as e:
            print('1', e)
            return e
        
    @property
    def payment_order_link(self):
        # return 'https://' + settings.SITE_DOMAIN + reverse('orders:order_review', args=[self.uuid])
        return reverse('payment:payment_invoice', args=[self.tracking_code])

    def receipt_received(self):
        self.order_status = self.AWAITING_CHECK
        self.save()

    def check_transfer_conditions(self, cart):
        setting = PaymentSetting.objects.get_first()
        if not setting.enable_transfer or self.payment_method != self.TRANSFER:
            raise Http404
        cart.clear()

    def check_wallet_conditions(self, cart, user):
        setting = PaymentSetting.objects.get_first()
        if not setting.enable_wallet or self.order_status != self.AWAITING_PAYMENT or self.payment_method != self.WALLET or self.user != user or self.payable > user.wallet.balance:
            raise Http404
        cart.clear()

    def check_post_paid_conditions(self, cart):
        setting = PaymentSetting.objects.get_first()
        if not setting.enable_post_paid or self.order_status != self.AWAITING_PAYMENT or self.payment_method != self.POST_PAID:
            raise Http404
        cart.clear()

    def complete_the_order(self, payment_method=None, cart=None):
        self.payment_method = payment_method if payment_method else self.BANK_GATEWAY
        if payment_method not in [self.POST_PAID]:
            self.paid = True
        else:
            print('no paid')

        self.order_status = self.DOING
        self.save()
        if self.discount_code:
            self.discount_code.increase_usage_count()
        Invoice.create(self)

        if cart:
            cart.clear()

    def waiting_to_confirm_order(self):
        self.order_status = self.AWAITING_CHECK
        self.save()

    @classmethod
    def get_status_name(cls, status):
        return ' ,'.join([str(v[1]) for v in cls.ORDER_STATUS_CHOICES if v[0] in status])

    def action_after_status_change(self, old_status, new_status, search_for_possible_status=False,
                                   first_time_create=False):
        if old_status == new_status:
            return self.WAREHOUSE_NO_CHANGE, None

        if first_time_create:
            order_status_changes = {
                (None, self.AWAITING_PAYMENT): self.WAREHOUSE_NO_CHANGE,
            }
        else:
            order_status_changes = {
                (None, self.DOING): self.WAREHOUSE_DECREASE,
                (None, self.AWAITING_CHECK): self.WAREHOUSE_DECREASE,
                (None, self.CANCELED): self.WAREHOUSE_NO_CHANGE,

                (self.AWAITING_PAYMENT, self.DOING): self.WAREHOUSE_DECREASE,
                (self.AWAITING_PAYMENT, self.AWAITING_CHECK): self.WAREHOUSE_DECREASE,
                (self.AWAITING_PAYMENT, self.CANCELED): self.WAREHOUSE_NO_CHANGE,

                (self.AWAITING_CHECK, self.CANCELED): self.WAREHOUSE_INCREASE,
                (self.AWAITING_CHECK, self.DOING): self.WAREHOUSE_NO_CHANGE,

                (self.DOING, self.PACKING): self.WAREHOUSE_NO_CHANGE,
                (self.DOING, self.DONE): self.WAREHOUSE_NO_CHANGE,
                (self.DOING, self.SENT): self.WAREHOUSE_NO_CHANGE,
                (self.DOING, self.CANCELED): self.WAREHOUSE_INCREASE,
                (self.DOING, self.RETURNED): self.WAREHOUSE_INCREASE,

                (self.PACKING, self.DONE): self.WAREHOUSE_NO_CHANGE,
                (self.PACKING, self.SENT): self.WAREHOUSE_NO_CHANGE,
                (self.PACKING, self.CANCELED): self.WAREHOUSE_INCREASE,
                (self.PACKING, self.RETURNED): self.WAREHOUSE_INCREASE,

                (self.DONE, self.CANCELED): self.WAREHOUSE_INCREASE,
                (self.DONE, self.RETURNED): self.WAREHOUSE_INCREASE,

                (self.SENT, self.DONE): self.WAREHOUSE_NO_CHANGE,
                (self.SENT, self.CANCELED): self.WAREHOUSE_INCREASE,
                (self.SENT, self.RETURNED): self.WAREHOUSE_INCREASE,

                (self.CANCELED, self.DOING): self.WAREHOUSE_DECREASE,
                (self.CANCELED, self.AWAITING_CHECK): self.WAREHOUSE_DECREASE,
                (self.CANCELED, self.AWAITING_PAYMENT): self.WAREHOUSE_NO_CHANGE,

                (self.RETURNED, self.DOING): self.WAREHOUSE_DECREASE,
                (self.RETURNED, self.AWAITING_CHECK): self.WAREHOUSE_DECREASE,
                (self.RETURNED, self.AWAITING_PAYMENT): self.WAREHOUSE_NO_CHANGE,
            }
        possible_status = [p[1] for p in order_status_changes.keys() if
                           p[0] == old_status] if search_for_possible_status else None
        current_change = (old_status, new_status)
        return order_status_changes.get(current_change, self.WAREHOUSE_FORBIDDEN), possible_status

    @admin.display(description=_('تاریخ واریز'), empty_value='-')
    def jdeposit_date(self):
        if self.deposit_date:
            return standard_jalali_datetime_format(self.deposit_date)
        return '-'

    jdeposit_date.admin_order_field = 'deposit_date'


class PackingType(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )

    class Meta:
        verbose_name = _('نوع بسته بندی')
        verbose_name_plural = _("انواع بسته بندی")

    def __str__(self):
        return self.name


class OrderItem(AbstractDateTimeModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('سفارش'),
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('محصول'),
    )
    product_category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('دسته بندی'),
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        verbose_name=_('تنوع محصول'),
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نام'),
    )
    price = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('قیمت'),
    )
    discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('تخفیف'),
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('تعداد'),
    )
    total_price = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('جمع کالاها'),
    )
    total_discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('جمع تخفیف'),
    )
    amount_payable = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('قابل پرداخت'),
    )

    class Meta:
        verbose_name = _('آیتم سفارش')
        verbose_name_plural = _('آیتم های سفارش')

    def __str__(self):
        return str(self.id)

    @property
    def get_price(self):
        return self.price if self.price else 0

    @property
    def get_discount(self):
        return self.discount if self.discount else 0

    @property
    def get_total_price(self):
        return self.quantity * self.get_price

    @property
    def get_total_discount(self):
        return self.quantity * self.get_discount

    @property
    def get_amount_payable(self):
        return self.get_total_price - self.get_total_discount

    @classmethod
    def create(cls, order_id, variant_items):
        for item in variant_items:
            cls.objects.create(
                order_id=order_id,
                variant=item.variant,
                quantity=item.quantity,
            )
            
    @classmethod
    def create_bulk(cls, order, items_data):
        order_items = []
        for item_data in items_data:
            variant = item_data['variant']
            quantity = item_data['quantity']
            order_item = cls(
                order=order,
                variant=variant,
                quantity=quantity
            )
            cls.calculate_price_and_set_values(order_item)
            order_items.append(order_item)
        cls.objects.bulk_create(order_items)

    @classmethod
    def calculate_price_and_set_values(cls, instance):
        variant = instance.variant
        product = instance.variant.product

        quantity = instance.quantity
        price = instance.price if instance.price else variant.price
        discount = instance.discount if instance.discount else variant.discount
        total_price = quantity * price
        total_discount = quantity * discount if discount else 0
        amount_payable = total_price - total_discount

        instance.variant = variant
        instance.product = product
        instance.product_id = variant.product_id
        instance.product_category = product.category.first()
        instance.name = variant.variant_descriptor

        instance.price = price
        instance.discount = discount
        instance.total_price = total_price
        instance.total_discount = total_discount
        instance.amount_payable = amount_payable


class Invoice(AbstractDateTimeModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('سفارش'),
    )
    tracking_code = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_('شماره پیگیری سفارش'),
    )
    through = models.CharField(
        max_length=50,
        verbose_name=_('از طریق'),
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('نام'),
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('نام خانوادگی'),
    )
    mobile_number = PhoneNumberField(
        max_length=50,
        verbose_name=_('شماره موبایل'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('ایمیل'),
    )
    province = models.CharField(
        max_length=200,
        verbose_name=_('استان')
    )
    city = models.CharField(
        max_length=200,
        verbose_name=_('شهر')
    )
    address = models.TextField(
        verbose_name=_('آدرس'),
    )
    postal_code = models.CharField(
        null=True,
        blank=True,
        verbose_name=_('کد پستی'),
        max_length=20
    )
    note = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('یادداشت'),
    )
    commodity_prices = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('قیمت کالاها'),
    )
    total_discount = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('تخفیف'),
    )
    discount_amount = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('مبلغ کوپن تخفیف'),
    )
    payable = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('قابل پرداخت'),
    )
    payment_method = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('روش پرداخت'),
    )
    order_created = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تاریخ ایجاد سفارش'),
    )

    class Meta:
        verbose_name = _('صورت حساب')
        verbose_name_plural = _('صورت حساب ها')

    def __str__(self):
        return f"{self.tracking_code}"

    # def admin_get_absolute_url(self):
    #     return reverse('admin:order_invoice_change', args=[self.id])

    def get_absolute_url(self):
        return reverse('orders:invoice', args=[self.id])

    def thermal_printer_absolute_url(self):
        return reverse('orders:thermal_printer_invoice', args=[self.id])

    @classmethod
    def create(cls, order):
        invoice = cls.objects.create(
            order_id=order.id,
            tracking_code=order.tracking_code,
            through=order.get_through_display(),
            first_name=order.first_name,
            last_name=order.last_name,
            mobile_number=order.mobile_number,
            email=order.email,
            province=order.province,
            city=order.city,
            address=order.address,
            postal_code=order.postal_code,
            note=order.note,
            commodity_prices=order.commodity_prices,
            total_discount=order.total_discount,
            discount_amount=order.discount_amount,
            payable=order.payable,
            payment_method=order.get_payment_method_display(),
            order_created=order.created,
        )
        InvoiceItem.create(invoice_id=invoice.id, items=order.orderitem_set.all())
        return invoice

    @property
    def complete_address(self):
        return f'{self.province}، {self.city}، {self.address}'

    @property
    @admin.display(description=_('نام و نام خانوادگی'))
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_items_number(self):
        return self.invoiceitem_set.aggregate(total_number=Sum('quantity'))['total_number']

    @admin.display(description=_('تاریخ ایجاد سفارش'), empty_value='-')
    def order_jcreated(self):
        if self.order_jcreated:
            return standard_jalali_datetime_format(self.order_created)


class InvoiceItem(AbstractDateTimeModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        verbose_name=_('صورت حساب'),
    )
    variant_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('شناسه')
    )
    product = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نام محصول'),
    )
    sku = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('شناسه SKU'),
    )
    price = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('قیمت'),
    )
    discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('تخفیف'),
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name=_('تعداد'),
    )
    total_price = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('جمع کالاها'),
    )
    total_discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('جمع تخفیف'),
    )
    amount_payable = models.PositiveBigIntegerField(
        blank=True,
        verbose_name=_('قابل پرداخت'),
    )

    class Meta:
        verbose_name = _('آیتم صورت حساب')
        verbose_name_plural = _('آیتم های صورت حساب')

    def __str__(self):
        return str(self.id)

    def get_sku(self):
        return self.sku if self.sku else '-'

    @classmethod
    def create(cls, invoice_id, items):
        for item in items:
            cls.objects.create(
                invoice_id=invoice_id,
                variant_id=item.variant_id,
                product=item.variant.variant_descriptor,
                sku=item.variant.get_sku,
                price=item.price,
                discount=item.discount if item.discount else 0,
                quantity=item.quantity,
                total_price=item.total_price,
                total_discount=item.total_discount,
                amount_payable=item.amount_payable,
            )

    @property
    def bold_quantity_in_invoice(self):
        if self.quantity > 1:
            return True
        if Variant.objects.filter(id=int(self.variant_id), product__type=Product.VARIABLE).exists():
            return True
        return False
    
    @property
    def final_price(self):
        if self.has_discount:
            return self.price - self.discount
        return self.price
    
    @property
    def has_discount(self):
        return True if self.discount else False
    
    @property
    def discount_percent(self):
        return 100 - round((self.price - self.discount) / self.price * 100) if self.discount else 0

    @property
    def price_after_discount(self):
        return self.final_price
    
    @property
    def price_before_discount(self):
        return self.price
