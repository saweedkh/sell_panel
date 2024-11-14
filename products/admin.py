# Django Built-in modules
from django.contrib import admin
from django.utils.html import mark_safe
from django.db.models import Q, F, Sum, Case, When, IntegerField
from django.db import models
from django.shortcuts import reverse
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

# Local Apps
from .forms import (
    ProductAdminForm,
    VariantInlineFormset,
    RelatedProductInlineFormset,
    ProductSpecificationInlineFormSet,
    AttributeInlineFormset,
)
from .models import (
    Product,
    Variant,
    Attribute,
    AttributeValue,
    Gallery,
    RelatedProduct,
    WarehouseCategory,
    Warehouse,
    Brand,
    Badge,
    Unit,
    ProductComment as Comment,
    ProductSettings as Settings,
    ProductSpecification,
)
from .resources import (
    ProductResource,
    VariantExportResource,
    VariantImportResource,
    WarehouseExportResource,
    WarehouseImportResource,
)
from orders.models import OrderItem, Order
from category.admin import CategoryMPTTAdminMixin
from comment.admin import CommentAdminMixin
from seo.admin import (
    SeoAdminMixin,
    ContentAdminMixin,
)

from utils.admin import DateTimeAdminMixin
from autosave.mixins import AdminAutoSaveMixin

# Third Party Packages
from mptt.admin import TreeRelatedFieldListFilter
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter
from import_export.admin import ExportActionModelAdmin, ExportMixin, ImportExportModelAdmin, \
    ImportExportActionModelAdmin
from import_export.formats import base_formats


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    autocomplete_fields = ('general_attribute', 'attribute_value',)
    extra = 0
    classes = ('collapse',)
    formset = ProductSpecificationInlineFormSet
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 40})
        },
    }

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ProductSpecificationInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super(ProductSpecificationInline, self).get_extra(request, obj, **kwargs)
        extra_count = request.GET.get('extra', None)
        if extra_count:
            extra = int(extra_count)
        return extra

class RelatedProductInline(SortableInlineAdminMixin, DynamicRawIDMixin, admin.TabularInline):
    formset = RelatedProductInlineFormset
    model = RelatedProduct
    fk_name = 'from_product'
    # autocomplete_fields = ('to_product',)
    dynamic_raw_id_fields = ('to_product',)
    classes = ('collapse',)
    extra = 0
    ordering = ('display_priority',)


class GalleryInline(admin.TabularInline):
    model = Gallery
    readonly_fields = ('display_gallery_image_thumbnail',)
    classes = ('collapse',)
    extra = 0

    @admin.display(description=_('نمایش تصویر'), empty_value='-')
    def display_gallery_image_thumbnail(self, obj):
        image_url = obj.get_image
        return mark_safe(f'''<a target="_blank" href="{image_url}">
        <img src="{image_url}" width="60" height="60" load="lazy" /></a>''')


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ('name', 'attribute_name',)

    class Media:
        js = ('admin/attribute_value/js/base.js',)
        
        
class VariantInline(DynamicRawIDMixin, admin.StackedInline):
    formset = VariantInlineFormset
    model = Variant
    exclude = ('product_name', 'variant_name', 'image')
    autocomplete_fields = ('attribute_values',)
    min_num = 1
    extra = 0
    
    


@admin.register(Variant)
class VariantAdmin(DynamicRawIDMixin, ImportExportActionModelAdmin):
    exclude = ('product_name',)
    list_display = ('display_product_name', 'reference_code', 'display_variant_image_thumbnail', 'sku', 'price',
                    'in_stock', 'sales', 'edit_product_page',)
    list_filter = ('in_stock', 'product__attributes', 'attribute_values', 'product__brand', 'default',)
    list_select_related = ('product',)
    readonly_fields = ('sales', *DateTimeAdminMixin.readonly_fields,)
    dynamic_raw_id_fields = ('product', 'attribute_values',)
    search_fields = ('product__name', 'sku', 'reference_code',)
    resource_classes = (VariantExportResource, VariantImportResource)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(
            Q(product__type=Product.SIMPLE, default=True) | Q(product__type=Product.VARIABLE) |
            Q(product__type=Product.DOWNLOADABLE, default=True) | Q(product__type=Product.VIRTUAL, default=True)
        ).select_related('product', )
        return queryset

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description=_('محصول'))
    def display_product_name(self, obj):
        if obj.product.type == Product.VARIABLE:
            return f"{obj.product.name} {obj.variant_name}"
        return obj.product.name

    @admin.display(description=_('تصویر'), empty_value='-')
    def display_variant_image_thumbnail(self, obj):
        image_url = obj.get_admin_image
        return mark_safe(f'''<a target="_blank" href="{image_url}">
        <img src="{image_url}" class="admin-image-box" width="50" height="50" load="lazy" /></a>''')

    @admin.display(description=_('نوع'))
    def display_product_type(self, obj):
        return obj.product.get_type_display()

    @admin.display(description=_('ویرایش محصول'))
    def edit_product_page(self, obj):
        return mark_safe(
            f'''<a target="_blank" href="{obj.product.product_admin_absolute_url()}">{_('ویرایش')}</a>''')



    


@admin.register(Product)
class ProductAdmin(AdminAutoSaveMixin, SortableAdminBase, DynamicRawIDMixin, ExportActionModelAdmin, ExportMixin):
    form = ProductAdminForm
    fieldsets = (  
        (_('محصول'), {'fields': (
            'name', 'extra_detail', 'type', 'attributes', 'brand', 'badge', 'unit', 'image',
        )}),
        (_('انبارداری'), {
            'fields': ('inventory_management',),
        }),

        *ContentAdminMixin.fieldsets,
        (_('نکات قبل از خرید'), {'fields': ('consider_before_buying',)}),
        *SeoAdminMixin.fieldsets,
        (_('تنظیمات بیشتر'), {
            'fields': ('related_items_display_status', 'autofill_related_items'),
            'classes': ('collapse',),
        }),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'in_stock',)
    list_display = ('name', *SeoAdminMixin.list_display, 'display_product_image_thumbnail',
                    'in_stock', 'inventory_management',)
    list_per_page = 20
    list_filter = (
        *SeoAdminMixin.list_filter,
        'type', 'in_stock', 'inventory_management', 'badge', 'brand',
    )
    search_fields = ('name', 'variant__sku',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ('attributes', 'badge', 'unit','brand',)
    # dynamic_raw_id_fields = ('brand',)
    inlines = (ProductSpecificationInline, VariantInline, GalleryInline, RelatedProductInline,
              *SeoAdminMixin.inlines,)
    actions = (*SeoAdminMixin.actions, 'enable_inventory_management', 'disable_inventory_management',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy
    save_on_top = True
    save_as = True
    resource_classes = [ProductResource, ]

    class Media:
        js = ('admin/product/js/base.js',)

    @admin.display(description=_('تصویر'), empty_value='-')
    def display_product_image_thumbnail(self, obj):
        image_url = obj.get_image
        return mark_safe(f'''<a target="_blank" href="{image_url}">
        <img src="{image_url}" class="admin-image-box" width="50" height="50" load="lazy" /></a>''')

    @admin.action(description=_('فعال کردن مدیریت موجودی'))
    def enable_inventory_management(modeladmin, request, queryset):
        for obj in queryset:
            obj.inventory_management = True
            obj.save()

    @admin.action(description=_('غیر فعال کردن مدیریت موجودی'))
    def disable_inventory_management(modeladmin, request, queryset):
        for obj in queryset:
            obj.inventory_management = False
            obj.save()


@admin.register(WarehouseCategory)
class WarehouseCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'display_inventory_count', 'display_inventory_items',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'display_inventory_count', 'display_inventory_items',)
    list_display = ('name', 'display_inventory_count', 'display_inventory_items',)
    search_fields = ('name',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy

    @admin.display(description=_('اقلام'), empty_value='-')
    def display_inventory_count(self, obj):
        return obj.warehouse_set.count()

    @admin.display(description=_('مشاهده اقلام'), empty_value='-')
    def display_inventory_items(self, obj):
        url = reverse(f'admin:{Warehouse._meta.app_label}_{Warehouse._meta.model_name}_changelist') + \
              f'?warehouse_category__id__exact={obj.pk}'
        return mark_safe(f'''<a target="_blank" href="{url}">{_('مشاهده')}</a>''')


@admin.register(Warehouse)
class WarehouseAdmin(NumericFilterModelAdmin, ImportExportActionModelAdmin):
    fieldsets = (
        (None,
         {'fields': ('warehouse_category', 'display_variant_name', 'quantity', 'temp_quantity', 'display_unit',
                     'without_order_limit', 'show_product_page')}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'display_variant_name', 'display_unit',
                       'show_product_page',)
    list_display = ('display_variant_name', 'display_sku', 'quantity', 'temp_quantity',
                    'display_unit', 'without_order_limit', 'count_in_doing_orders', 'count_in_awaiting_check_orders',
                    'count_in_all_orders',)
    list_select_related = ('variant', 'product__unit')
    list_editable = ('quantity', 'temp_quantity', 'without_order_limit',)
    list_filter = (
        'warehouse_category',
        'without_order_limit',
        ('quantity', RangeNumericFilter),
        ('temp_quantity', RangeNumericFilter),
    )
    search_fields = ('product__name', 'warehouse_category__name',)
    autocomplete_fields = ('warehouse_category',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy
    resource_classes = (WarehouseExportResource, WarehouseImportResource,)

    class Media:
        js = ('admin/product/js/warehouse.js',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        try:
            request.GET = request.GET.copy()
            product_pk = request.GET.pop('product_pk', None)
            if product_pk:
                product_pk = int(product_pk[0])
                queryset = queryset.filter(product=product_pk)
        except Exception as exp:
            pass

        qs = queryset.annotate(
            doing_orders=Sum(
                Case(
                    When(variant__orderitem__order__order_status=Order.DOING, then=F('variant__orderitem__quantity')),
                    output_field=IntegerField()
                )
            ),
            awaiting_check_orders=Sum(
                Case(
                    When(variant__orderitem__order__order_status=Order.AWAITING_CHECK,
                         then=F('variant__orderitem__quantity')),
                    output_field=IntegerField()
                )
            )
        )
        return qs

    @admin.display(description=_('محصول'), empty_value='-')
    def display_variant_name(self, obj):
        return obj.variant.variant_descriptor

    @admin.display(description=_('شناسه SKU'), empty_value='-')
    def display_sku(self, obj):
        return obj.variant.get_sku

    @admin.display(description=_('واحد'), empty_value='-')
    def display_unit(self, obj):
        return obj.product.unit if obj.product.unit else '-'

    @admin.display(description=_('درحال انجام'), empty_value=0)
    def count_in_doing_orders(self, obj):
        return obj.doing_orders

    count_in_doing_orders.admin_order_field = 'doing_orders'

    @admin.display(description=_('انتظار بررسی'), empty_value=0)
    def count_in_awaiting_check_orders(self, obj):
        return obj.awaiting_check_orders

    count_in_awaiting_check_orders.admin_order_field = 'awaiting_check_orders'

    @admin.display(description=_('مجموع'), empty_value=0)
    def count_in_all_orders(self, obj):
        doing_orders = obj.doing_orders if obj.doing_orders else 0
        awaiting_check_orders = obj.awaiting_check_orders if obj.awaiting_check_orders else 0
        return doing_orders + awaiting_check_orders

    @admin.display(description=_('مشاهده محصول'))
    def show_product_page(self, obj):
        return mark_safe(
            f'''<a target="_blank" href="{obj.product.product_admin_absolute_url()}">{_('مشاهده')}</a>''')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Brand)
class BrandAdmin(AdminAutoSaveMixin, admin.ModelAdmin):
    fieldsets = (
        (_('برند'), {'fields': ('name', 'image',)}),
        *ContentAdminMixin.fieldsets,
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name', *SeoAdminMixin.list_display, *DateTimeAdminMixin.list_display,)
    list_filter = (*SeoAdminMixin.list_filter,)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = (*SeoAdminMixin.inlines,)
    actions = (*SeoAdminMixin.actions,)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy


class AttributeValueInline(SortableInlineAdminMixin, admin.TabularInline):
    formset = AttributeInlineFormset
    model = AttributeValue
    exclude = ('attribute_name',)
    ordering = ('display_priority',)
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(SortableAdminBase, admin.ModelAdmin):
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name', *DateTimeAdminMixin.list_display,)
    search_fields = ('name',)
    inlines = (AttributeValueInline,)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('برچسب'), {'fields': ('name', 'badge_color', 'text_color',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name', 'display_badge', *DateTimeAdminMixin.list_display,)
    search_fields = ('name',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy

    @admin.display(description=_('برچسب'), empty_value='-')
    def display_badge(self, obj):
        return mark_safe(
            f'''<label class="product-badge-display" style="color: {obj.text_color};background-color: {obj.badge_color};">
            {obj.name}</label>''')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('واحد'), {'fields': ('name',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name', *DateTimeAdminMixin.list_display,)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(CommentAdminMixin):
    fieldsets = (
        (None, {'fields': (
            'product',
        )}),
        *CommentAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = (
        *CommentAdminMixin.list_display,
        *DateTimeAdminMixin.list_display,
    )
    list_filter = (*CommentAdminMixin.list_filter,)
    search_fields = (*CommentAdminMixin.search_fields,)
    # autocomplete_fields = (*CommentAdminMixin.autocomplete_fields, 'product')
    dynamic_raw_id_fields = (*CommentAdminMixin.dynamic_raw_id_fields, 'product')
    date_hierarchy = DateTimeAdminMixin.date_hierarchy


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('display_page_title',)
    fieldsets = (
        (None, {'fields': (
            'paginator_number', 'related_items_display_status', 'related_items_number', 'autofill_related_items')}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_('تنظیمات'), empty_value='-')
    def display_page_title(self, obj):
        return obj.__str__()
