# Django Built-in modules
from django.db import models
from django.db.models import F, Q, Sum
from django.db import transaction
from django.templatetags.static import static
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

# Local apps
from comment.models import AbstractBaseComment
from utils.models import AbstractDateTimeModel
from category.models import AbstractBaseCategory
from seo.models import AbstractBaseSeoModel, AbstractContentModel
from setting.models import SiteGlobalSetting
from .mixins import ModelDiffMixin
from .utils import ProductSortChoices, make_automatic_description


# Third Party Packages
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from smart_selects.db_fields import ChainedForeignKey



class ProductQueryset(models.QuerySet):

    def published(self):
        return self.filter(page_display_status=AbstractBaseSeoModel.PUBLISH).select_related('badge', ).order_by(
            '-in_stock')


class Product(ModelDiffMixin, AbstractContentModel, AbstractBaseSeoModel, AbstractDateTimeModel):
    SIMPLE = 0
    VARIABLE = 1
    DOWNLOADABLE = 2
    VIRTUAL = 3
    PRODUCT_TYPE_STATUS_CHOICES = (
        (SIMPLE, _('ساده')),
        (VARIABLE, _('متنوع')),
        (DOWNLOADABLE, _('دانلودی')),
        (VIRTUAL, _('مجازی')),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    extra_detail = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('جزئیات بیشتر'),
        help_text=_('جزئیات بیشتر درباره محصول مانند جنس، تعداد در بسته و...'),
    )
    image = models.ImageField(
        max_length=255,
        null=True,
        blank=True,
        upload_to='products/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(350, 300)],
        format='JPEG',
        options={'quality': 60}
    )
    type = models.PositiveSmallIntegerField(
        choices=PRODUCT_TYPE_STATUS_CHOICES,
        default=SIMPLE,
        verbose_name=_('نوع محصول'),
    )
    attributes = models.ManyToManyField(
        'Attribute',
        blank=True,
        verbose_name=_('ویژگی ها'),
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('برند'),
    )
    badge = models.ForeignKey(
        'Badge',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('برچسب'),
    )
    unit = models.ForeignKey(
        'Unit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('واحد'),
    )
    inventory_management = models.BooleanField(
        default=False,
        verbose_name=_('مدیریت موجودی'),
    )
    in_stock = models.BooleanField(
        default=True,
        verbose_name=_('در انبار'),
    )
    related_products = models.ManyToManyField(
        'self',
        blank=True,
        through='RelatedProduct',
        symmetrical=False,
        verbose_name=_('محصولات مرتبط'),
    )
    related_items_display_status = models.BooleanField(
        default=True,
        verbose_name=_('نمایش موارد مرتبط'),
    )
    autofill_related_items = models.BooleanField(
        default=True,
        verbose_name=_('پر کردن خودکار محصولات مرتبط')
    )

    consider_before_buying = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('نکات قبل از خرید')
    )

    objects = ProductQueryset.as_manager()

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.__attributes___ = None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        print(reverse('products:product-detail', args=[self.id])
)
        return reverse('products:product-detail', args=[self.id])

    def preview_absolute_url(self):
        return reverse('products:product_preview', args=[self.id])

    def submit_comment_absolute_url(self):
        return reverse('ajax:comment_product_submit', args=[self.id])

    def submit_reply_absolute_url(self):
        return reverse('ajax:reply_product_submit', args=[self.id])

    def load_product_specifications_absolute_url(self):
        return f"{reverse('admin:product_product_change', args=[self.id])}?extra={len(self.get_specifications())}"

    def product_admin_absolute_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])

    def product_warehouse_absolute_url(self):
        return reverse(
            f'admin:{self._meta.app_label}_{Warehouse._meta.model_name}_changelist') + f'?product_pk={self.pk}'\
            

    def get_short_description(self):
        if not self.description:
            short_description = make_automatic_description(self.content)
            self.description = short_description
            self.save()
        return self.description
    
    @property
    def get_comment_count(self):
        return ProductComment.objects.filter(product=self.id).count()

    @property
    def default_search_engine_title(self):
        return self.name

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def structured_data(self):
        site_url = settings.SITE_DOMAIN
        site_setting = SiteGlobalSetting.get_default_setting()
        default_variant = self.default_variant
        availability = "https://schema.org/InStock" if self.in_stock else "https://schema.org/OutOfStock"
        data = [
            {
                "@context": "https://schema.org/",
                "@type": "Product",
                "name": self.name,
                "image": f"https://{site_url}{self.get_image}",
                "description": self.search_engine_description,
                "sku": f'{self.pk}',
                "mpn": self.pk,
                "offers": {
                    "@type": "Offer",
                    "url": f'https://{site_url}{self.get_absolute_url()}',
                    "priceCurrency": "IRR",
                    "price": f"{default_variant.price}",
                    "availability": availability,
                },
                "review": []
            }
        ]
        if self.brand:
            data[0]["brand"] = {"@type": "Brand", "name": self.brand.name},
        else:
            data[0]["brand"] = {"@type": "Brand", "name": site_setting.name},

        return data

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
            else : 
                image = static('defaults/default.png')
        except:
            image = static('defaults/default.png')
        return image
    
    @property
    def get_api_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
        except:
            image = None
        return image

    @property
    def is_variable(self):
        return True if self.type == self.VARIABLE else False

    @property
    def default_variant(self):
        default = self.variant_set.filter(default=True).first()
        if not default or not default.in_stock:
            default = self.variant_set.order_by(
                '-in_stock',
                '-warehouse__quantity',
                'warehouse__without_order_limit',
                'price'
            ).first()
            
        return default

    @property
    def get_attributes(self):

        if self.type != self.VARIABLE:
            return None, None, None

        variant_attributes = self.variant_set.values(
            variant_id=F("id"),
            attribute_id=F("attribute_values__attribute_id"),
            attribute__name=F("attribute_values__attribute_name"),
            attribute_value_id=F("attribute_values"),
            attribute_value__name=F("attribute_values__name"),
            attribute_value__color=F("attribute_values__color"),
            attribute_value__pattern=F("attribute_values__pattern"),
        )

        all_attributes_and_values_set = dict()
        attribute_values_colors_or_patterns = dict()
        variant_attributes_and_values = dict()

        for item in variant_attributes:
            variant_id = item.get('variant_id')
            attribute = (item.get('attribute_id'), item.get('attribute__name'))
            value = (item.get('attribute_value_id'), item.get('attribute_value__name'))
            color_or_pattern = (item.get('attribute_value_id'), item.get('attribute_value__color'),
                                item.get('attribute_value__pattern'))

            if all_attributes_and_values_set.get(attribute):
                all_attributes_and_values_set[attribute].add(value)
            else:
                all_attributes_and_values_set[attribute] = {value, }

            if variant_attributes_and_values.get(variant_id):
                variant_attributes_and_values[variant_id][attribute] = value
            else:
                variant_attributes_and_values[variant_id] = {attribute: value}

            if attribute_values_colors_or_patterns.get(attribute):
                attribute_values_colors_or_patterns[attribute].add(color_or_pattern)
            else:
                attribute_values_colors_or_patterns[attribute] = {color_or_pattern, }

        return all_attributes_and_values_set, variant_attributes_and_values, attribute_values_colors_or_patterns

    @property
    def get_all_attribute_values(self):
        queryset = self.variant_set.values('id', 'attribute_values')
        result = {}
        for item in queryset:
            variant_id = item.get('id')
            attribute_value_ids = item.get('attribute_values')
            if result.get(variant_id):
                result[variant_id].add(attribute_value_ids)
            else:
                result[variant_id] = {attribute_value_ids}
        return result

    @property
    def get_attributes_input_types(self):
        if self.type != self.VARIABLE:
            return None

        attributes_input_types = dict()

        for attr in self.attributes.all():
            attributes_input_types[attr.id] = attr.input_field_type

        return attributes_input_types
    
    


    def get_gallery(self, variant):
        product_gallery = list()
        if self.image:
            product_gallery.append((self, 0))
        [product_gallery.append((gallery_image, 0)) for gallery_image in self.gallery.all()]
        slider_position = 0

        if variant:
            if self.type == self.VARIABLE:
                for product_variant in self.variant_set.all():
                    if product_variant.image:
                        product_gallery.append((product_variant, product_variant.pk))

            for i, element in enumerate(product_gallery):
                slide, source = element
                if source == variant.pk:
                    slider_position = i
                    break

        return slider_position, product_gallery

    def track_fields_for_signal(self):
        return 'name' in self.changed_fields

    def find_variant_by_attribute_values(self, selected):
        attribute_values = self.get_all_attribute_values
        for variant_id, attribute_value_ids in attribute_values.items():
            if attribute_value_ids == set(selected):
                return Variant.objects.get(id=variant_id)
        return None

    def remove_wishlist_absolute_url(self):
        return reverse('account:wishlist_remove', args=[self.id])

    def add_wishlist_absolute_url(self):
        return reverse('ajax:wishlist_add', args=[self.id])

    def get_related_products(self):
        setting = ProductSettings.objects.get_first()

        if not setting.related_items_display_status or not self.related_items_display_status:
            return []

        num = setting.related_items_number

        related_objects = self.related_products.filter(page_display_status=AbstractBaseSeoModel.PUBLISH, in_stock=True).order_by(
            'related_to__display_priority')
        if setting.autofill_related_items and self.autofill_related_items:
            result = list(related_objects)
            id_list = [self.id]
            id_list.extend(list(related_objects.values_list('id', flat=True)))
            remaining = num - related_objects.count()


            objects = Product.objects.filter(
                in_stock=True,
                page_display_status=AbstractBaseSeoModel.PUBLISH
            ).order_by('?').exclude(id__in=id_list).distinct()
            result.extend(list(objects)[:remaining])
            return result
        else:
            return related_objects[:num]

    def check_in_stock_status(self, automatic_status_update=True):
        if self.inventory_management:
            status = self.warehouse_set.filter(
                Q(without_order_limit=False, quantity__gt=0) | Q(without_order_limit=True)
            ).exists()
        elif self.type == Product.VARIABLE:
            status = self.variant_set.filter(in_stock=True).exists()
        else:
            status = self.variant_set.filter(in_stock=True, default=True).exists()
        if automatic_status_update:
            self.in_stock = status
            self.save()
        return status

    def truncated_name(self):
        return ' '.join(self.name.split()[:3])


    @property
    def get_consider_before_buying(self):
        if self.consider_before_buying:
            return self.consider_before_buying
        category = self.category.first()
        if category.consider_before_buying:
            return category.consider_before_buying


class Attribute(ModelDiffMixin, AbstractDateTimeModel):
    SIMPLE_RADIO_BUTTON = 1
    PATTERNED_RADIO_BUTTON = 2
    COLORED_RADIO_BUTTON = 3
    DROP_DOWN = 4
    INPUT_FIELD_TYPE_CHOICES = (
        (SIMPLE_RADIO_BUTTON, _('دکمه رادیویی ساده')),
        (PATTERNED_RADIO_BUTTON, _('دکمه رادیویی با طرح')),
        (COLORED_RADIO_BUTTON, _('دکمه رادیویی با رنگ')),
        (DROP_DOWN, _('منوی کشویی')),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('نام'),
    )
    input_field_type = models.PositiveSmallIntegerField(
        choices=INPUT_FIELD_TYPE_CHOICES,
        default=DROP_DOWN,
        verbose_name=_('نوع فیلد ورودی'),
    )

    class Meta:
        verbose_name = _('ویژگی')
        verbose_name_plural = _('ویژگی ها')

    def __str__(self):
        return self.name

    def track_fields_for_signal(self):
        return 'name' in self.changed_fields


class AttributeValue(AbstractDateTimeModel):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name=_('ویژگی'),
    )
    attribute_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نام'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )
    display_priority = models.PositiveIntegerField(
        db_index=True,
        default=0,
        verbose_name=_('اولویت نمایش'),
    )
    color = ColorField(
        null=True,
        blank=True,
        verbose_name=_('رنگ'),
    )
    pattern = models.ImageField(
        null=True,
        blank=True,
        upload_to='attributes/',
        verbose_name=_('طرح'),
    )

    class Meta:
        verbose_name = _('مقدار ویژگی')
        verbose_name_plural = _('مقادیر ویژگی')
        ordering = ('attribute', 'display_priority',)

    def __str__(self):
        return f'{self.attribute_name}: {self.name}'


class Variant(ModelDiffMixin, AbstractDateTimeModel):
    reference_code = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('کد ارجاع'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
    )
    product_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نام محصول'),
    )
    variant_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('نام تنوع'),
    )
    sku = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_('شناسه SKU')
    )
    attribute_values = models.ManyToManyField(
        AttributeValue,
        blank=True,
        verbose_name=_('مقدار ویژگی ها'),
    )
    buying_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('قیمت خرید'),
    )
    price = models.PositiveBigIntegerField(
        verbose_name=_('قیمت'),
    )
    discount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('تخفیف'),
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='products/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 60}
    )
    in_stock = models.BooleanField(
        default=True,
        verbose_name=_('در انبار'),
    )
    order_limit_max = models.PositiveIntegerField(
        default=0,
        help_text=_('0 به معنی عدم محدودیت'),
        verbose_name=_('محدودیت سفارش (حداکثر)'),
    )
    order_limit_min = models.PositiveIntegerField(
        default=1,
        help_text=_('1 به معنی عدم محدودیت'),
        verbose_name=_('محدودیت سفارش (حداقل)'),
    )
    default = models.BooleanField(
        default=False,
        verbose_name=_('پیشفرض'),
    )
    sales = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_('فروش'),
    )

    class Meta:
        verbose_name = _('تنوع محصول')
        verbose_name_plural = _('تنوع محصولات')

    def __str__(self):
        return str(self.id)

    @property
    def get_sku(self):
        return self.sku if self.sku else '-'

    @property
    def in_stock_status(self):
        if self.in_stock:
            if self.product.inventory_management:
                warehouse = self.warehouse
                if not warehouse.without_order_limit and warehouse.quantity <= 0:
                    return False
                return True
            return True
        return False

    @property
    def variant_descriptor(self):
        product = self.product
        if product.type == Product.VARIABLE:
            return f'{self.product_name} {self.variant_name}'
        return self.product_name

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

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
        except:
            image = None
        return image

    @property
    def get_admin_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
        except:
            try:
                product = self.product
                if product.image.url and product.image_thumbnail.url and product.image.file:
                    image = product.image_thumbnail.url
            except:
                image = static('defaults/default.png')
        return image

    def validation_to_add_to_cart(self, quantity):
        try:
            try:
                quantity = int(quantity)
            except ValueError:
                raise CartException(_('یک مقدار معتبر برای تعداد محصول وارد کنید.'))
            if quantity < 1:
                raise CartException(_('حداقل تعداد مجاز برای افزودن به سبد خرید برابر با ۱ است.'))
            if not self.in_stock:
                raise CartException(_('{0} موجود نیست.'.format(self.variant_descriptor)))
            if not self.order_limit_max == 0 and self.order_limit_max < quantity:
                if self.product.unit:
                    raise CartException(
                        _('سقف تعداد سفارش برای {0}، {1} {2} می باشد.'.format(
                            self.variant_descriptor, self.order_limit_max, self.product.unit.name)
                        )
                    )
                else:
                    raise CartException(
                        _('سقف تعداد سفارش برای {0}، {1} عدد می باشد.'.format(
                            self.variant_descriptor, self.order_limit_max)
                        )
                    )
            if not self.order_limit_min <= 1 and self.order_limit_min > quantity:
                if self.product.unit:
                    raise CartException(
                        _('حداقل تعداد سفارش برای {0}، {1} {2} می باشد.'.format(
                            self.variant_descriptor, self.order_limit_min, self.product.unit.name)
                        )
                    )
                else:
                    raise CartException(
                        _('حداقل تعداد سفارش برای {0}، {1} عدد می باشد.'.format(
                            self.variant_descriptor, self.order_limit_min)
                        )
                    )

            try:
                warehouse = self.warehouse
            except Warehouse.DoesNotExist:
                warehouse = None
            if warehouse and not warehouse.without_order_limit and quantity > warehouse.quantity:
                if warehouse.quantity <= 0:
                    raise CartException(
                        _('{} در انبار موجود نیست.'.format(self.variant_descriptor))
                    )
                raise CartException(
                    _('سقف تعداد سفارش برای {0}، {1} عدد می باشد.'.format(self.variant_descriptor, warehouse.quantity))
                )
        except CartException as exception:
            raise exception

    def validation_before_payment(self, quantity):
        msg = None
        try:
            if not self.in_stock:
                msg = _('{0} موجود نیست.'.format(self.variant_descriptor))

            if not self.order_limit_max == 0 and self.order_limit_max < quantity:
                if self.product.unit:
                    msg = _('سقف تعداد سفارش برای {0}، {1} {2} می باشد.'.format(
                        self.variant_descriptor, self.order_limit_max, self.product.unit.name)
                    )
                else:
                    msg = _('سقف تعداد سفارش برای {0}، {1} عدد می باشد.'.format(
                        self.variant_descriptor, self.order_limit_max)
                    )

            if not self.order_limit_min <= 1 and self.order_limit_min > quantity:
                if self.product.unit:
                    msg = _('حداقل تعداد سفارش برای {0}، {1} {2} می باشد.'.format(
                        self.variant_descriptor, self.order_limit_min, self.product.unit.name)
                    )
                else:
                    msg = _('حداقل تعداد سفارش برای {0}، {1} عدد می باشد.'.format(
                        self.variant_descriptor, self.order_limit_min)
                    )

            try:
                warehouse = self.warehouse
            except Warehouse.DoesNotExist:
                warehouse = None
            if warehouse and not warehouse.without_order_limit and quantity > warehouse.quantity:
                if warehouse.quantity <= 0:
                    msg = _('{} در انبار موجود نیست.'.format(self.variant_descriptor))
                else:
                    msg = _('سقف تعداد سفارش برای {0}، {1} عدد می باشد.'.format(
                        self.variant_descriptor, warehouse.quantity))

        except CartException as exception:
            raise exception

        return msg


class WarehouseCategory(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )

    class Meta:
        verbose_name = _('انبار')
        verbose_name_plural = _('انبار ها')

    def __str__(self):
        return self.name


class Warehouse(AbstractDateTimeModel):
    warehouse_category = models.ManyToManyField(
        WarehouseCategory,
        blank=True,
        verbose_name=_('انبار'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
    )
    variant = models.OneToOneField(
        Variant,
        on_delete=models.CASCADE,
        verbose_name=_('تنوع محصول'),
    )
    quantity = models.IntegerField(
        verbose_name=_('موجودی'),
        default=0,
    )
    temp_quantity = models.IntegerField(
        verbose_name=_('موجودی ثانویه'),
        null=True,
        blank=True,
        default=0,
    )
    without_order_limit = models.BooleanField(
        default=True,
        verbose_name=_('بدون محدودیت سفارش'),
    )

    class Meta:
        verbose_name = _('موجودی')
        verbose_name_plural = _('موجودی ها')

    def __str__(self):
        return str(self.pk)

    @classmethod
    def increase_quantity(cls, order_items):
        with transaction.atomic():
            for item in order_items:
                try:
                    warehouse_record = cls.objects.get(variant_id=item['variant_id'])
                    warehouse_record.quantity = warehouse_record.quantity + item['quantity']
                    warehouse_record.save()
                except cls.DoesNotExist:
                    pass

    @classmethod
    def decrease_quantity(cls, order_items):
        with transaction.atomic():
            for item in order_items:
                try:
                    warehouse_record = cls.objects.get(variant_id=item['variant_id'])
                    warehouse_record.quantity = warehouse_record.quantity - item['quantity']
                    warehouse_record.save()
                except cls.DoesNotExist:
                    pass

    @classmethod
    def create_records(cls, variants):
        bulk_list = [cls(product_id=item.product_id, variant_id=item.id) for item in variants]
        cls.objects.bulk_create(bulk_list)

    @classmethod
    def delete_single_records(cls, variant_id):
        cls.objects.filter(variant_id=variant_id).delete()

    @classmethod
    def delete_records(cls, product_id):
        cls.objects.filter(product_id=product_id).delete()


class Gallery(AbstractDateTimeModel):
    product = models.ForeignKey(
        Product,
        related_name='gallery',
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
    )
    image = models.ImageField(
        max_length=255,
        upload_to='products/%y/%m/%d/',
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 60}
    )
    alt = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('تگ آلت'),
    )

    class Meta:
        verbose_name = _('گالری محصول')
        verbose_name_plural = _('گالری محصول')

    def __str__(self):
        return str(self.id)

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image.url
        except:
            image = static('defaults/default.png')

        return image
    
    @property
    def get_api_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image.url
        except:
            image = None

        return image

    def get_alt(self):
        return self.alt if self.alt else self.product.name


class RelatedProduct(AbstractDateTimeModel):
    from_product = models.ForeignKey(
        Product,
        related_name='related_from',
        on_delete=models.CASCADE,
    )
    to_product = models.ForeignKey(
        Product,
        related_name='related_to',
        verbose_name=_('محصول'),
        on_delete=models.CASCADE,
    )
    display_priority = models.PositiveIntegerField(
        db_index=True,
        default=0,
        verbose_name=_('اولویت نمایش'),
    )

    class Meta:
        verbose_name = _("محصول مرتبط")
        verbose_name_plural = _("محصولات مرتبط")
        ordering = ('display_priority',)

    def __str__(self):
        return str(self.display_priority)


class Brand(AbstractContentModel, AbstractBaseSeoModel, AbstractDateTimeModel):
    name = models.CharField(
        max_length=250,
        verbose_name=_('نام'),
    )
    image = models.ImageField(
        upload_to='brands/%y/%m/%d/',
        null=True,
        blank=True,
        verbose_name=_('تصویر'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(70, 70)],
        format='JPEG',
        options={'quality': 60}
    )

    class Meta:
        verbose_name = _('برند')
        verbose_name_plural = _('برند ها')

    def __str__(self):
        return self.name

    @property
    def default_search_engine_title(self):
        return self.name

    @property
    def default_search_engine_description(self):
        return None

    @property
    def default_search_engine_keywords(self):
        return None

    @property
    def get_image(self):
        try:
            if self.image.url and self.image_thumbnail.url and self.image.file:
                image = self.image_thumbnail.url
        except:
            image = static('defaults/default.png')

        return image

    def get_absolute_url(self):
        return reverse('products:brand', args=[self.slug])


class Badge(AbstractDateTimeModel):
    name = models.CharField(
        max_length=250,
        verbose_name=_('نام'),
    )
    badge_color = ColorField(
        default='#FF0000',
        verbose_name=_('رنگ برچسب'),
    )
    text_color = ColorField(
        default='#FFFFFF',
        verbose_name=_('رنگ متن'),
    )

    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب ها')

    def __str__(self):
        return self.name


class Unit(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('نام'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('واحد')
        verbose_name_plural = _('واحد ها')


class ProductComment(AbstractBaseComment, AbstractDateTimeModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
    )

    class MPTTMeta:
        order_insertion_by = ('-created',)

    class Meta:
        verbose_name = _('نظر')
        verbose_name_plural = _('نظرات')

    def __str__(self):
        return self.name

    def admin_reply_absolute_url(self):
        return reverse("product:reply_comment", args=[self.id])

    def admin_edit_absolute_url(self):
        return reverse("admin:product_productcomment_change", args=[self.id])

    def product_absolute_url(self):
        return reverse("product:product", args=[self.product.slug])


class ProductSettingsQueryset(models.QuerySet):
    def get_first(self):
        setting = self.first()
        if not setting:
            setting = self.create()
        return setting


class ProductSettings(AbstractDateTimeModel):
    related_items_display_status = models.BooleanField(
        default=True,
        verbose_name=_('نمایش محصولات مرتبط'),
    )
    related_items_number = models.PositiveSmallIntegerField(
        default=10,
        verbose_name=_('تعداد محصولات مرتبط'),
    )
    autofill_related_items = models.BooleanField(
        default=True,
        verbose_name=_('پر کردن خودکار محصولات مرتبط')
    )
    paginator_number = models.PositiveSmallIntegerField(
        default=12,
        verbose_name=_('تعداد محصول در هر صفحه دسته بندی'),
    )

    objects = ProductSettingsQueryset.as_manager()

    class Meta:
        verbose_name = _('پیکربندی محصولات')
        verbose_name_plural = _('پیکربندی محصولات')

    def __str__(self):
        return str(_('پیکربندی محصولات'))


class ProductSpecificationQueryset(models.QuerySet):
    def specials(self):
        return self.filter(show_in_product_description=True)


class ProductSpecification(AbstractDateTimeModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('محصول'),
    )
    general_attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name=_('ویژگی'),
    )
    attribute_value = models.ManyToManyField(
        AttributeValue,
        blank=True,
        verbose_name=_('مقدار ویژگی'),
    )
    custom_attribute_value = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('مقدار ویژگی (دلخواه)')
    )
    show_in_product_description = models.BooleanField(
        default=False,
        verbose_name=_('نمایش در توضیحات محصول'),
    )

    objects = ProductSpecificationQueryset.as_manager()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = _('مشخصات محصول')
        verbose_name_plural = _('مشخصات محصول')