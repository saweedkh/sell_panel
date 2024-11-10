# Django Built-in modules
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import Receipt, PaymentSetting, Card
from .forms import ReceiptAdminForm, ReceiptInlineFormset, CardInlineFormset, PaymentSettingAdminForm
from utils.admin import DateTimeAdminMixin


class ReceiptInline(admin.StackedInline):
    model = Receipt
    formset = ReceiptInlineFormset
    fields = ('amount', 'status', 'image', 'tracking_code', 'download_receipt_image',)
    readonly_fields = ('download_receipt_image',)
    extra = 0
    classes = ('collapse',)

    @admin.display(description=_('مشاهده تصویر'))
    def download_receipt_image(self, obj):
        if obj.image and obj.image_thumbnail:
            return mark_safe(
                f'<a href="{obj.image.url}" target="_blank"><img height="50" src="{obj.image_thumbnail.url}"/></a>')
        return '-'

    def has_add_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    form = ReceiptAdminForm
    fieldsets = (
        (None, {'fields': ('order',)}),
        (_('اطلاعات رسید'), {'fields': ('amount', 'image', 'tracking_code', 'status',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('order', 'amount', 'status', *DateTimeAdminMixin.list_display)
    list_select_related = ('order',)
    list_filter = ('status', *DateTimeAdminMixin.list_filter)
    search_fields = ('order__tracking_code',)
    autocomplete_fields = ('order',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy


class CardInline(admin.StackedInline):
    model = Card
    fields = ('fullname', 'bank_name', 'bank_logo', 'get_bank_logo', 'card_number', 'shaba', 'account_number', 'active',
              *DateTimeAdminMixin.fields)
    readonly_fields = ('get_bank_logo', *DateTimeAdminMixin.readonly_fields,)
    formset = CardInlineFormset
    extra = 0

    @admin.display(description=_('مشاهده لوگو'))
    def get_bank_logo(self, obj):
        if obj.bank_logo and obj.bank_logo.file:
            return mark_safe(f'<img height="50" src="{obj.bank_logo_thumbnail.url}"/>')
        return '-'


@admin.register(PaymentSetting)
class PaymentSettingAdmin(admin.ModelAdmin):
    form = PaymentSettingAdminForm
    fieldsets = (
        (_('پرداخت از درگاه بانکی'), {'fields': ('enable_gateway',)}),
        # (_('پرداخت کارت به کارت'), {'fields': ('enable_transfer', 'transfer_content',)}),
        # (_('پرداخت از کیف پول'), {'fields': ('enable_wallet',)}),
        (_('پرداخت در محل'), {'fields': ('enable_post_paid', 'prepayment_status_for_post_paid',
                                         'prepayment_percentage',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('display_page_title',)
    # inlines = (CardInline,)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_('تنظیمات'), empty_value='-')
    def display_page_title(self, obj):
        return obj.__str__()
