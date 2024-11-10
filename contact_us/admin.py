# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import ContactUsMessages
from utils.admin import DateTimeAdminMixin


@admin.register(ContactUsMessages)
class ContactUsMessagesAdmin(admin.ModelAdmin):
    list_display = ('type', 'fullname', 'phone', 'subject', 'jcreated', 'is_checked',)
    fieldsets = (
        (None, {'fields': ('type', 'fullname', 'phone', 'email', 'subject', 'message',)}),
        (_('وضعیت درخواست'), {'fields': ('is_checked',)}),
        *DateTimeAdminMixin.fieldsets,
    )
    list_filter = ('type', 'is_checked',)
    list_editable = ('is_checked',)
    search_fields = ('fullname', 'email', 'phone', 'subject', 'message',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    actions = ('change_checked_to_true', 'change_checked_to_false',)

    @admin.action(description=_('تغییر به بررسی شده'))
    def change_checked_to_true(modeladmin, request, queryset):
        queryset.update(is_checked=True)

    @admin.action(description=_('تغییر به بررسی نشده'))
    def change_checked_to_false(modeladmin, request, queryset):
        queryset.update(is_checked=False)
