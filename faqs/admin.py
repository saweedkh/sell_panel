# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import (
    Category as FAQCategory,
    FAQItems,
    TermsCategory,
    TermsItems
)

# Third Party Packages
from dynamic_raw_id.admin import DynamicRawIDMixin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(FAQCategory)
class FAQCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'display',)
    list_filter = ('display',)
    list_editable = ('display',)
    search_fields = ('name',)


@admin.register(FAQItems)
class FAQItemsAdmin(DynamicRawIDMixin, TabbedTranslationAdmin):
    list_display = ('category', 'question', 'display',)
    list_select_related = ('category',)
    list_filter = ('display', 'category',)
    search_fields = ('question',)
    # autocomplete_fields = ('category',)
    dynamic_raw_id_fields = ('category',)
    actions = ('change_display_to_true', 'change_display_to_false',)

    @admin.action(description=_('تغییر وضعیت به نمایش'))
    def change_display_to_true(modeladmin, request, queryset):
        queryset.update(display=True)

    @admin.action(description=_('تغییر وضعیت به عدم نمایش'))
    def change_display_to_false(modeladmin, request, queryset):
        queryset.update(display=False)


@admin.register(TermsCategory)
class TermsCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'display',)
    list_filter = ('display',)
    list_editable = ('display',)
    search_fields = ('name',)


@admin.register(TermsItems)
class TermsItemsAdmin(DynamicRawIDMixin, TabbedTranslationAdmin):
    list_display = ('category', 'name', 'display',)
    list_select_related = ('category',)
    list_filter = ('display', 'category',)
    search_fields = ('name', 'description',)
    # autocomplete_fields = ('category',)
    dynamic_raw_id_fields = ('category',)
    actions = ('change_display_to_true', 'change_display_to_false',)

    @admin.action(description=_('تغییر وضعیت به نمایش'))
    def change_display_to_true(modeladmin, request, queryset):
        queryset.update(display=True)

    @admin.action(description=_('تغییر وضعیت به عدم نمایش'))
    def change_display_to_false(modeladmin, request, queryset):
        queryset.update(display=False)
