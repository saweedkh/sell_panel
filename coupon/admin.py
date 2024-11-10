# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.admin import DateTimeAdminMixin
from .models import (
    DiscountCoupon,
)
from .forms import DiscountCouponAdminForm

# Third Party Packages
from dynamic_raw_id.admin import DynamicRawIDMixin


@admin.register(DiscountCoupon)
class DiscountCouponAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    form = DiscountCouponAdminForm
    fieldsets = (
        (_('کوپن تخفیف'), {'fields': ('code', 'type', 'amount', 'description', 'active'), }),
        (_('مبلغ سبد خرید'), {'fields': ('minimum_spend', 'maximum_spend',), }),
        (_('محصولات'), {'fields': ('products', 'exclude_products',), }),
        (_('دسته بندی ها'), {'fields': ('categories', 'exclude_categories',), }),
        (_('بازه زمانی'), {'fields': ('valid_from', 'valid_to',), }),
        (_('تعداد استفاده'), {'fields': ('usage_limit_per_coupon', 'usage_count',), }),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'usage_count')
    list_display = ('code', 'description', 'type', 'amount', 'active', *DateTimeAdminMixin.list_display,)
    list_filter = ('type', 'active', 'valid_from', 'valid_to',)
    search_fields = ('code', 'description',)
    # dynamic_raw_id_fields = (
    #     'products',
    #     'exclude_products',
    #     'categories',
    #     'exclude_categories',
    # )
    actions = ('make_active', 'make_inactive',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy
    save_on_top = True
    autocomplete_fields = (
        'products',
        'exclude_products',
        'categories',
        'exclude_categories',
    )

    class Media:
        js = ('admin/coupon/js/generate_random_code.js',)
        css = {
            'all': ('admin/coupon/css/generate_random_code.css',)
        }

    # Actions
    @admin.action(description=_('تغییر وضعیت به فعال'))
    def make_active(modeladmin, request, queryset):
        queryset.update(active=True)

    @admin.action(description=_('تغییر وضعیت به غیر فعال'))
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)
