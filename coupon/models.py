# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel
from products.models import (
    Product,
)

# # Python Standard Library
from django.utils import timezone


class DiscountException(Exception):
    pass


class DiscountCoupon(AbstractDateTimeModel):
    PERCENTAGE_DISCOUNT = 1
    FIXED_CART_DISCOUNT = 2

    TYPE_CHOICES = (
        (PERCENTAGE_DISCOUNT, _('درصد')),
        (FIXED_CART_DISCOUNT, _('مقدار ثابت')),
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name=_('کد'),
    )
    type = models.SmallIntegerField(
        choices=TYPE_CHOICES,
        default=PERCENTAGE_DISCOUNT,
        verbose_name=_('نوع'),
    )
    amount = models.PositiveBigIntegerField(
        verbose_name=_('درصد / مبلغ'),
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('توضیحات'),
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_('فعال'),
    )
    minimum_spend = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('حداقل مبلغ سبد خرید'),
    )
    maximum_spend = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('حداکثر مبلغ سبد خرید'),
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='products',
        verbose_name=_('شامل این محصولات'),
    )
    exclude_products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='exclude_products',
        verbose_name=_('به غیر از این محصولات'),
    )
   
    valid_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('معتبر از'),
    )
    valid_to = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('معتبر تا'),
    )
    usage_limit_per_coupon = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('محدودیت تعداد استفاده'),
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('تعداد استفاده'),
    )

    class Meta:
        verbose_name = _('کوپن تحفیف')
        verbose_name_plural = _("کوپن های تخفیف")

    def __str__(self):
        return self.code

    @property
    def get_description(self):
        if self.description:
            return self.description
        return _('کوپن تخفیف') + ' ' + self.code

    def active_validation(self):
        if not self.active:
            raise DiscountException(_('این کوپن تخفیف دیگر فعال نیست.'))

    def minimum_spend_validation(self, amount=None):
        if amount and self.minimum_spend and self.minimum_spend > amount:
            raise DiscountException(
                _('حداقل مبلغ سبد خرید برای استفاده از این کوپن %s تومان می باشد.' % f"{self.minimum_spend:,}"))

    def maximum_spend_validation(self, amount=None):
        if amount and self.maximum_spend and self.maximum_spend < amount:
            raise DiscountException(
                _('حداکثر مبلغ سبد خرید برای استفاده از این کوپن %s تومان می باشد.' % f"{self.maximum_spend:,}"))

    def products_validation(self, products=None):
        if products and self.products.count() > 0:
            difference_of_products = set(products) - set(self.products.all())
            name_of_products = [product.name for product in difference_of_products]
            if name_of_products:
                raise DiscountException(_('این کوپن تخفیف شامل %s نمی شود.' % f"{','.join(name_of_products)}"))

    def exclude_products_validation(self, products=None):
        if products and self.exclude_products.count() > 0:
            intersection_of_products = set(self.exclude_products.all()) & set(products)
            name_of_products = [product.name for product in intersection_of_products if product in products]
            if name_of_products:
                raise DiscountException(_('این کوپن تخفیف شامل %s نمی شود.' % f"{','.join(name_of_products)}"))

    def categories_validation(self, categories=None):
        if categories and self.categories.count() > 0:
            difference_of_categories = set(categories) - set(self.categories.all())
            name_of_categories = [category.name for category in difference_of_categories]
            if name_of_categories:
                raise DiscountException(
                    _('این کوپن تخفیف شامل محصولات دسته بندی %s نمی شود.' % f"{','.join(name_of_categories)}"))

    def exclude_categories_validation(self, categories=None):
        if categories and self.exclude_categories.count() > 0:
            intersection_of_categories = set(self.exclude_categories.all()) & set(categories)
            name_of_categories = [category.name for category in intersection_of_categories if category in categories]
            if name_of_categories:
                raise DiscountException(
                    _('این کوپن تخفیف شامل محصولات دسته بندی %s نمی شود.' % f"{','.join(name_of_categories)}"))

    def date_validation(self):
        now = timezone.now()
        if self.valid_from and self.valid_to:
            if not self.valid_from < now < self.valid_to:
                raise DiscountException(_('این کوپن تخفیف در این بازه زمانی معتبر نیست.'))
        if not self.valid_from and self.valid_to:
            if not now < self.valid_to:
                raise DiscountException(_('این کوپن تخفیف در این بازه زمانی معتبر نیست.'))

    def usage_limit_per_coupon_validation(self):
        if self.usage_limit_per_coupon and self.usage_limit_per_coupon <= self.usage_count:
            raise DiscountException(_('محدودیت استفاده از این کوپن تخفیف به پایان رسیده.'))

    def validation(self, amount=None, products=None, categories=None, brands=None):
        self.active_validation()
        self.date_validation()
        self.usage_limit_per_coupon_validation()
        self.minimum_spend_validation(amount=amount)
        self.maximum_spend_validation(amount=amount)
        self.products_validation(products=products)
        self.exclude_products_validation(products=products)
        self.categories_validation(categories=categories)
        self.exclude_categories_validation(categories=categories)

    def calculate_discount(self, amount):
        amount = int(amount)
        if self.type == self.FIXED_CART_DISCOUNT:
            final_price = self.amount
        elif self.type == self.PERCENTAGE_DISCOUNT:
            final_price = int((self.amount / 100) * amount)
        else:
            raise DiscountException(_('این کوپن تخفیف معتبر نیست.'))
        return final_price

    def increase_usage_count(self):
        self.usage_count = self.usage_count + 1
        self.save()
