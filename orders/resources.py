# Django Built-in modules
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import (
    Order,
)

# Third Party Packages
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, DateTimeWidget


class OrderResource(resources.ModelResource):
    id = fields.Field(
        column_name=_('شناسه'),
        attribute='id',
    )
    tracking_code = fields.Field(
        column_name=_('شماره پیگیری'),
        attribute='tracking_code',
    )
    through = fields.Field(
        column_name=_('از طریق'),
        attribute='get_through_display',
    )
    order_status = fields.Field(
        column_name=_('وضعیت سفارش'),
        attribute='get_order_status_display',
    )
    first_name = fields.Field(
        column_name=_('نام'),
        attribute='first_name',
    )
    last_name = fields.Field(
        column_name=_('نام خانوادگی'),
        attribute='last_name',
    )
    mobile_number = fields.Field(
        column_name=_('شماره موبایل'),
        attribute='mobile_number',
    )
    province = fields.Field(
        column_name=_('استان'),
        attribute='province',
    )
    city = fields.Field(
        column_name=_('شهر'),
        attribute='city',
    )
    address = fields.Field(
        column_name=_('آدرس'),
        attribute='address',
    )
    postal_code = fields.Field(
        column_name=_('کد پستی'),
        attribute='postal_code',
    )
    note = fields.Field(
        column_name=_('یادداشت سفارش'),
        attribute='note',
    )
    payable = fields.Field(
        column_name=_('قابل پرداخت'),
        attribute='payable',
    )
    payment_method = fields.Field(
        column_name=_('روش پرداخت'),
        attribute='get_payment_method_display',
    )
    created = fields.Field(
        column_name=_('تاریخ ایجاد سفارش'),
        attribute='created',
        widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    class Meta:
        model = Order
        fields = (
            'created', 'payment_method', 'payable', 'note', 'postal_code',
            'address', 'city', 'province', 'mobile_number', 'last_name', 'first_name', 'order_status', 'through',
            'tracking_code', 'id',
        )
        export_order = fields[::-1]

    def dehydrate_created(self, obj):
        try:
            split_date = obj.jcreated().split(' ')
            split_date.reverse()
            return ' '.join(split_date)
        except Exception as exp:
            return obj.created.strftime('%Y-%m-%d %H:%M:%S')
