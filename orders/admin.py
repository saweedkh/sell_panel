# Django Built-in modules
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.forms import Textarea
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from django.conf.urls.static import static

# Python Standard Libraries
import json

# Local Apps
from account.models import User
from .models import (
    Order,
    PackingType,
    OrderItem,
    Invoice,
    InvoiceItem,
)
from .forms import OrderItemAdminForm, OrderItemInlineFormset, OrderAdminForm
from .utils import change_orders_status
from .resources import OrderResource
from payment.admin import ReceiptInline
from utils.admin import DateTimeAdminMixin
from django.conf import settings

# Third Party Packages
from django_json_widget.widgets import JSONEditorWidget
from dynamic_raw_id.admin import DynamicRawIDMixin
from gateways import models as bank_models
from import_export.admin import ExportActionModelAdmin, ExportMixin
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class OrderItemInline(DynamicRawIDMixin, admin.StackedInline):
    model = OrderItem
    form = OrderItemAdminForm
    formset = OrderItemInlineFormset
    fields = (
        'variant', 'name', 'quantity', 'display_price', 'display_discount', 'display_total_price', 'display_customer',
        'display_amount_payable',
    )
    readonly_fields = (
        'name', 'display_price', 'display_discount', 'display_total_price', 'display_customer',
        'display_amount_payable',
    )
    dynamic_raw_id_fields = ('variant',)
    min_num = 1
    extra = 0

    def has_add_permission(self, request, obj):
        if obj and obj.order_status not in (Order.AWAITING_PAYMENT,):
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if obj and obj.order_status not in (Order.AWAITING_PAYMENT,):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.order_status not in (Order.AWAITING_PAYMENT,):
            return False
        return True

    @admin.display(description=_('قیمت'))
    def display_price(self, obj):
        return obj.get_price

    @admin.display(description=_('تخفیف'))
    def display_discount(self, obj):
        return obj.get_discount

    @admin.display(description=_('جمع کالاها'))
    def display_total_price(self, obj):
        return obj.get_total_price

    @admin.display(description=_('جمع تخفیف'))
    def display_customer(self, obj):
        return obj.get_total_discount

    @admin.display(description=_('قابل پرداخت'))
    def display_amount_payable(self, obj):
        return obj.get_amount_payable


class TransactionsAdminInline(GenericTabularInline):
    model = bank_models.Bank
    fields = ('status', 'bank_type', 'amount', 'reference_number', 'response_result', 'extra_information',)
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 80})
        },
    }
    classes = ('collapse',)
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class InvoiceInline(admin.TabularInline):
    model = Invoice
    fields = ('display_invoice_link', 'thermal_print_invoice_link', 'print_invoice_link', 'payable', 'created',)
    readonly_fields = ('display_invoice_link', 'thermal_print_invoice_link', 'print_invoice_link', 'created', 'payable')
    classes = ('collapse',)
    extra = 0

    @admin.display(description=_('مشاهده صورت حساب'))
    def display_invoice_link(self, obj):
        if obj.id:
            return mark_safe(
                format_html(
                    u'<a style="direction:ltr;" href="{}">{}</a>',
                    obj.admin_get_absolute_url(), _('مشاهده')
                )
            )
        return '-'

    @admin.display(description=_('چاپ صورتحساب'))
    def print_invoice_link(self, obj):
        return mark_safe(
            format_html(
                u'<a href="{}" target="_blank"><button type="button">{}</button></a>',
                obj.get_absolute_url(), _('چاپ')
            )
        )

    @admin.display(description=_('چاپ صورتحساب حرارتی'))
    def thermal_print_invoice_link(self, obj):
        return mark_safe(
            format_html(
                u'<a href="{}" target="_blank"><button type="button">{}</button></a>',
                obj.thermal_printer_absolute_url(), _('چاپ')
            )
        )

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PaidStatusFilter(SimpleListFilter):
    title = _('وضعیت پرداخت')
    parameter_name = 'paid_status'

    def lookups(self, request, model_admin):
        return [(1, _('پرداخت نشده')), (2, _('پرداخت شده')), (3, _('در انتظار تایید'))]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(paid=False)
        if self.value() == '2':
            return queryset.filter(paid=True)
        if self.value() == '3':
            return queryset.filter(paid=False, payment_method=Order.TRANSFER, order_status=Order.AWAITING_CHECK)


class AbandonedStatusFilter(SimpleListFilter):
    title = _('سفارشات رها شده')
    parameter_name = 'abandoned'

    def lookups(self, request, model_admin):
        return [(0, _('سفارشات رها شده')), (1, _('همه سفارشات')), ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(
                Q(order_status=Order.AWAITING_PAYMENT) |
                (Q(order_status=Order.AWAITING_CHECK) & Q(receipt__isnull=True))
            )
        if self.value() == '1':
            return queryset



@admin.register(Order)
class OrderAdmin(DynamicRawIDMixin, ExportActionModelAdmin, ExportMixin):
    form = OrderAdminForm
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
        models.DateField: {'form_class': JalaliDateField, 'widget': AdminJalaliDateWidget},
        models.DateTimeField: {'form_class': SplitJalaliDateTimeField, 'widget': AdminSplitJalaliDateTime},
    }
    fieldsets = (
        (_('سفارش'), {'fields': (
            'user', 'through', 'tracking_code', 'reference_code', 'postal_tracking_code', 'order_status',
            'packing_type', 'send_notification_sms', 'mark_order', 
            # 'register_in_accounting_system',
        )}),
        (_('اطلاعات مشتری'), {'fields': (
            'first_name', 'last_name', 'mobile_number', 'email', 'province_id', 'city_id', 'address', 'postal_code',
            'note',
        )}),

        (_('کوپن تخفیف'), {'fields': (
            'discount_code',
        )}),
        (_('جزئیات صورتحساب'), {'fields': (
            'commodity_prices', 'discount_amount', 'total_discount',
        )}),
        (_('قابل پرداخت'), {'fields': (
            'display_payment_order_link', 'display_payable', 'prepayment'
        )}),
        (_('جزئیات پرداخت'), {'fields': (
            'payment_method', 'paid', 'deposit_date',
        )}),
        (_('جزئیات دستگاه'), {
            'fields': ('user_agent', 'user_ip',),
            'classes': ('collapse',),
        }),
        *DateTimeAdminMixin.fieldsets,
    )
    list_display = (
        'display_customer',
        'display_mobile_number',
        'order_status',
        'display_paid_status',
        'payable',
        'jcreated',
        'jupdated',
    )
    list_filter = (
        PaidStatusFilter,
        'through',
        'order_status',
        'payment_method',
        'packing_type',
        'mark_order',
        'register_in_accounting_system',
        AbandonedStatusFilter,
        'province_id',
    )
    search_fields = ('tracking_code', 'reference_code', 'first_name', 'last_name', 'mobile_number', 'email',
                     'province', 'city', 'postal_code',)
    readonly_fields = (
        'tracking_code', 'reference_code', 'commodity_prices', 'discount_amount', 'total_discount',
        'display_payable', 'display_payment_order_link', *DateTimeAdminMixin.readonly_fields,
        'user_ip'
    )
    dynamic_raw_id_fields = ('user', 'discount_code',)
    autocomplete_fields = ('province_id', 'city_id', 'packing_type',)
    inlines = (OrderItemInline, TransactionsAdminInline, ReceiptInline, InvoiceInline,)
    actions = ('print_labels', 'change_status_to_packing', 'change_status_to_done', 'change_status_to_sent',)
    save_on_top = True
    resource_classes = [OrderResource, ]

    class Media:
        js = ('admin/order/js/base.js',)
        css = {
            'all': ('admin/order/css/custom.css',)
        }

    # save seller user as registrar
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.registrar = request.user
            obj.save()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return list_filter

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request)
        if not obj or obj.order_status not in (Order.AWAITING_PAYMENT, Order.AWAITING_CHECK):
            readonly_fields = list(readonly_fields)
            readonly_fields.append('prepayment')
        return readonly_fields

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.request = request
        return form

    def save_formset(self, request, form, formset, change):
        formset.save()  # this will save the children
        form.instance.save()  # form.instance is the parent

    def show_or_hide_postal_tracking_code_field(self, request):
        list_editable = list(self.list_editable)
        list_display = list(self.list_display)
        postal_tracking_code_field = 'postal_tracking_code'
        for param, value in request.GET.items():
            if param == 'order_status__exact' and value == str(Order.PACKING):
                list_editable.append(postal_tracking_code_field)
                list_display.append(postal_tracking_code_field)
                list_display = sorted(set(list_display), key=list_display.index)
                list_editable = sorted(set(list_editable), key=list_editable.index)
                return list_display, list_editable

        if postal_tracking_code_field in list_display:
            list_display = list(filter(postal_tracking_code_field.__ne__, list_display))
            list_display = sorted(set(list_display), key=list_display.index)
        if postal_tracking_code_field in list_editable:
            list_editable = list(filter(postal_tracking_code_field.__ne__, list_editable))
            list_editable = sorted(set(list_editable), key=list_editable.index)
        return list_display, list_editable

    def changelist_view(self, request, extra_context=None):
        list_display, list_editable = self.show_or_hide_postal_tracking_code_field(request)
        self.list_display = list_display
        self.list_editable = list_editable
        return super().changelist_view(request, extra_context)

    @admin.display(description=_('مشتری'))
    def display_customer(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description=_('قابل پرداخت'))
    def display_payable(self, obj):
        return obj.get_payable_in_post_paid

    @admin.display(description=_('شماره تلفن'))
    def display_mobile_number(self, obj):
        return f"0{obj.mobile_number.national_number}"

    @admin.display(description=_('وضعیت پرداخت'))
    def display_paid_status(self, obj):
        if obj.paid:
            return mark_safe(format_html('<img src="/static/admin/img/icon-yes.svg" alt="True" load="lazy"/>', ))
        else:
            if obj.order_status == Order.AWAITING_CHECK and obj.payment_method == Order.TRANSFER and obj.receipt_set.exists():
                return mark_safe(
                    format_html(
                        '<img src="/static/admin/img/icon-alert.svg" alt="False" load="Waiting"/>'))
            return mark_safe(
                format_html('<img src="/static/admin/img/icon-no.svg" alt="False" load="lazy"/>', ))

    display_paid_status.admin_order_field = 'paid'

    @admin.display(description=_('استان/شهر'))
    def display_province_and_city(self, obj):
        return f"{obj.province}، {obj.city}"

    @admin.display(description=_('لینک پرداخت سفارش'))
    def display_payment_order_link(self, obj):
        if obj.is_payable:
            return mark_safe(
                format_html(
                    u'<p id="display_payment_link" style="direction:ltr;">{}</p> <button onclick="copyToClipboard()" type="button">{}</button>',
                    obj.payment_order_link, _('کپی لینک')
                )
            )
        return _('غیرفعال (سفارش پرداخت شده)')

    # Change status to Packing
    @admin.action(description=_('تغییر وضعیت سفارش به بسته بندی'))
    def change_status_to_packing(modeladmin, request, queryset):
        status = Order.PACKING
        change_orders_status(queryset, status)

    # Change status to Done
    @admin.action(description=_('تغییر وضعیت سفارش به تکمیل شده'))
    def change_status_to_done(modeladmin, request, queryset):
        status = Order.DONE
        change_orders_status(queryset, status)

    # Change status to Sent
    @admin.action(description=_('تغییر وضعیت سفارش به ارسال شده'))
    def change_status_to_sent(modeladmin, request, queryset):
        status = Order.SENT
        change_orders_status(queryset, status)

    
    # change_form_template = 'admin/order/order/change_form.html'
    

@admin.register(PackingType)
class PackingTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    search_fields = ('name',)


class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem

    readonly_fields = (
        'variant_id', 'product', 'price', 'discount', 'quantity', 'total_price', 'total_discount',
        'amount_payable',
    )
    min_num = 1
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('اطلاعات سفارش'), {'fields': (
            'order', 'tracking_code', 'order_jcreated', 'through',
        )}),
        (_('اطلاعات مشتری'), {'fields': (
            'first_name', 'last_name', 'mobile_number', 'email',
        )}),
        (_('آدرس'), {'fields': (
            'province', 'city', 'address', 'postal_code', 'note',
        )}),
        (_('جزئیات صورتحساب'), {'fields': (
            'commodity_prices', 'discount_amount', 'total_discount', 'payable'
        )}),
        (_('جزئیات پرداخت'), {'fields': (
            'payment_method',
        )}),
        *DateTimeAdminMixin.fieldsets,
    )
    list_display = (
        'tracking_code', 'fullname', 'mobile_number', 'province', 'city', 'payable', 'order_jcreated',)
    autocomplete_fields = ('order',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'tracking_code', 'order_jcreated',)
    list_filter = ('through', 'province', 'city', 'payment_method', 'order_created',)
    search_fields = ('tracking_code', 'first_name', 'last_name', 'mobile_number')
    inlines = (InvoiceItemInline,)
    actions = ('print_invoices',)

    def has_add_permission(self, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description=_('چاپ صورت حساب های انتخاب شده'))
    def print_invoices(self, request, queryset):
        context = {
            'invoices': queryset,
            'site_url': settings.SITE_DOMAIN
        }
        return render(request, 'order/invoice_batch_print.html', context)