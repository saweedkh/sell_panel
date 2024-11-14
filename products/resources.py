# Django Built-in modules
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import (
    Product,
    Variant,
    Attribute,
    Brand,
    Badge,
    Unit,
    Warehouse,
)

# Third Party Packages
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, DateTimeWidget


class ProductResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    name = fields.Field(
        column_name=_('نام'),
        attribute='name',
    )
    extra_detail = fields.Field(
        column_name=_('جزئیات بیشتر'),
        attribute='extra_detail',
    )
    price = fields.Field(
        column_name=_('قیمت در سایت'),
    )
    type = fields.Field(
        column_name=_('نوع محصول'),
        attribute='get_type_display',
    )
    attributes = fields.Field(
        column_name=_('ویژگی ها'),
        attribute='attributes',
        widget=ManyToManyWidget(Attribute, separator='، ', field='name')
    )
    brand = fields.Field(
        column_name=_('برند'),
        attribute='brand',
        widget=ForeignKeyWidget(Brand, 'name')
    )
    badge = fields.Field(
        column_name=_('برچسب'),
        attribute='badge',
        widget=ForeignKeyWidget(Badge, 'name')
    )
    unit = fields.Field(
        column_name=_('واحد'),
        attribute='unit',
        widget=ForeignKeyWidget(Unit, 'name')
    )
    inventory_management = fields.Field(
        column_name=_('مدیریت موجودی'),
        attribute='inventory_management',
    )
    in_stock = fields.Field(
        column_name=_('در انبار'),
        attribute='in_stock',
    )
    created = fields.Field(
        column_name=_('تاریخ ایجاد'),
        attribute='created',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    updated = fields.Field(
        column_name=_('تاریخ بروزرسانی'),
        attribute='updated',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    class Meta:
        model = Product
        fields = (
            'updated', 'created', 'in_stock', 'inventory_management', 'unit', 'badge', 'brand', 'attributes',
            'type', 'price', 'extra_detail', 'name', 'category', 'id',
        )
        export_order = fields[::-1]

    def dehydrate_price(self, obj):
        variant = obj.default_variant
        return variant.final_price

    def dehydrate_created(self, obj):
        try:
            split_date = obj.jcreated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.created.strftime('%Y-%m-%d %H:%M:%S')

    def dehydrate_updated(self, obj):
        try:
            split_date = obj.jupdated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.updated.strftime('%Y-%m-%d %H:%M:%S')


class VariantExportResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    product_name = fields.Field(
        column_name=_('نام محصول'),
        attribute='product_name',
    )
    variant_name = fields.Field(
        column_name=_('تنوع'),
        attribute='variant_name',
    )
    reference_code = fields.Field(
        column_name=_('کد ارجاع'),
        attribute='reference_code',
    )
    sku = fields.Field(
        column_name=_('شناسه SKU'),
        attribute='sku',
    )
    buying_price = fields.Field(
        column_name=_('قیمت خرید'),
        attribute='buying_price',
    )
    price = fields.Field(
        column_name=_('قیمت'),
        attribute='price',
    )
    discount = fields.Field(
        column_name=_('تخفیف'),
        attribute='discount',
    )
    in_stock = fields.Field(
        column_name=_('در انبار'),
        attribute='in_stock',
    )
    order_limit_max = fields.Field(
        column_name=_('محدودیت سفارش (حداکثر)'),
        attribute='order_limit_max',
    )
    order_limit_min = fields.Field(
        column_name=_('محدودیت سفارش (حداقل)'),
        attribute='order_limit_min',
    )
    default = fields.Field(
        column_name=_('پیشفرض'),
        attribute='default',
    )
    created = fields.Field(
        column_name=_('تاریخ ایجاد'),
        attribute='created',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    updated = fields.Field(
        column_name=_('تاریخ بروزرسانی'),
        attribute='updated',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    class Meta:
        name = '---'
        model = Variant
        fields = (
            'updated', 'created', 'default', 'order_limit_min', 'order_limit_max', 'in_stock', 'discount',
            'price', 'buying_price', 'sku', 'reference_code', 'variant_name', 'product_name', 'id',
        )
        export_order = fields[::-1]
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)

    def dehydrate_created(self, obj):
        try:
            split_date = obj.jcreated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.created.strftime('%Y-%m-%d %H:%M:%S')

    def dehydrate_updated(self, obj):
        try:
            split_date = obj.jupdated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.updated.strftime('%Y-%m-%d %H:%M:%S')


class VariantImportResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    reference_code = fields.Field(
        column_name=_('کد ارجاع'),
        attribute='reference_code',
        default=None,
    )
    sku = fields.Field(
        column_name=_('شناسه SKU'),
        attribute='sku',
        default=None,
    )
    buying_price = fields.Field(
        column_name=_('قیمت خرید'),
        attribute='buying_price',
        default=None,
    )
    price = fields.Field(
        column_name=_('قیمت'),
        attribute='price',
    )
    discount = fields.Field(
        column_name=_('تخفیف'),
        attribute='discount',
        default=None,
    )
    in_stock = fields.Field(
        column_name=_('در انبار'),
        attribute='in_stock',
    )
    order_limit_max = fields.Field(
        column_name=_('محدودیت سفارش (حداکثر)'),
        attribute='order_limit_max',
    )
    order_limit_min = fields.Field(
        column_name=_('محدودیت سفارش (حداقل)'),
        attribute='order_limit_min',
    )

    class Meta:
        name = _('تنوع محصول')
        model = Variant
        fields = ('order_limit_min', 'order_limit_max', 'in_stock', 'discount', 'price', 'buying_price', 'sku', 'id',)
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ("id",)

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.dry_run = dry_run


class WarehouseExportResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    product_name = fields.Field(
        column_name=_('نام محصول'),
        attribute='variant',
        widget=ForeignKeyWidget(Variant, 'product_name')
    )
    variant_name = fields.Field(
        column_name=_('تنوع'),
        attribute='variant',
        widget=ForeignKeyWidget(Variant, 'variant_name')
    )
    quantity = fields.Field(
        column_name=_('موجودی'),
        attribute='quantity',
    )
    without_order_limit = fields.Field(
        column_name=_('بدون محدودیت سفارش'),
        attribute='without_order_limit',
    )
    created = fields.Field(
        column_name=_('تاریخ ایجاد'),
        attribute='created',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    updated = fields.Field(
        column_name=_('تاریخ بروزرسانی'),
        attribute='updated',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    class Meta:
        name = '---'
        model = Warehouse
        fields = (
            'updated', 'created', 'without_order_limit', 'quantity', 'variant_name', 'product_name', 'id',
        )
        export_order = fields[::-1]

    def dehydrate_created(self, obj):
        try:
            split_date = obj.jcreated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.created.strftime('%Y-%m-%d %H:%M:%S')

    def dehydrate_updated(self, obj):
        try:
            split_date = obj.jupdated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.updated.strftime('%Y-%m-%d %H:%M:%S')


class WarehouseImportResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    quantity = fields.Field(
        column_name=_('موجودی'),
        attribute='quantity',
    )
    without_order_limit = fields.Field(
        column_name=_('بدون محدودیت سفارش'),
        attribute='without_order_limit',
    )

    class Meta:
        name = _('انبار')
        model = Warehouse
        fields = ('without_order_limit', 'quantity', 'id',)
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ("id",)

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.dry_run = dry_run
