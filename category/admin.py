# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from mptt.admin import DraggableMPTTAdmin
from dynamic_raw_id.admin import DynamicRawIDMixin


class CategoryMPTTAdminMixin(DynamicRawIDMixin, DraggableMPTTAdmin):
    fieldsets = (
        (_('دسته بندی'), {'fields': ('parent', 'name',)}),
    )
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',)
    list_display_links = ('indented_title',)
    autocomplete_fields = ('parent',)
    # dynamic_raw_id_fields = ('parent',)
    search_fields = ('name',)
