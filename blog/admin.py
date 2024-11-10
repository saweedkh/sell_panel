# Django Built-in modules
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from category.admin import CategoryMPTTAdminMixin
# Local Apps
from .forms import RelatedPostInlineFormset
from .models import (
    AbstractBlogCategory,
    AbstractBlogPost,
    RelatedPost,
    AbstractBlogPostSettings as Settings,
)
from seo.admin import (
    SeoAdminMixin,
    ContentAdminMixin,
)
from utils.admin import DateTimeAdminMixin
from autosave.mixins import AdminAutoSaveMixin

# Third Party Packages
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from dynamic_raw_id.admin import DynamicRawIDMixin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


# @admin.register(Category)
class BlogCategoryAdminMixin(AdminAutoSaveMixin, CategoryMPTTAdminMixin, TabbedTranslationAdmin):
    fieldsets = (
        *CategoryMPTTAdminMixin.fieldsets,
        (_('توضیحات و تصویر'), {'fields': ('short_description', 'image', 'icon',)}),
        *ContentAdminMixin.fieldsets,
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,

    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = (
        *CategoryMPTTAdminMixin.list_display, *
        SeoAdminMixin.list_display,
        *DateTimeAdminMixin.list_display,
    )
    list_filter = (*SeoAdminMixin.list_filter,)
    search_fields = (*CategoryMPTTAdminMixin.search_fields,)
    prepopulated_fields = {"slug": ("name",)}
    # autocomplete_fields = (*CategoryMPTTAdminMixin.autocomplete_fields,)
    dynamic_raw_id_fields = (*CategoryMPTTAdminMixin.dynamic_raw_id_fields,)
    inlines = (*SeoAdminMixin.inlines,)
    actions = (*SeoAdminMixin.actions,)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy
    save_on_top = False


# @admin.register(Category)
# class CategoryAdmin(TranslationAdmin, AdminAutoSaveMixin):
#     fieldsets = (
#         (None, {'fields': ('name', 'image',)}),
#         (_('پیشنمایش'), {'fields': (
#             'display_image_thumbnail',
#         )}),
#         *ContentAdminMixin.fieldsets,
#         *SeoAdminMixin.fieldsets,
#         *DateTimeAdminMixin.fieldsets,
#     )
#     readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'display_image_thumbnail',)
#     list_display = (
#         'name',
#         *SeoAdminMixin.list_display,
#         *DateTimeAdminMixin.list_display,
#     )
#     list_filter = (*SeoAdminMixin.list_filter,)
#     search_fields = ('name',)
#     prepopulated_fields = {"slug": ("name",)}
#     inlines = (*SeoAdminMixin.inlines,)
#     actions = (*SeoAdminMixin.actions,)
#     save_on_top = False
#
#     @admin.display(description=_('تصویر'), empty_value='-')
#     def display_image_thumbnail(self, obj):
#         image_url = obj.get_image
#         return mark_safe(f'''<a target="_blank" href="{image_url}">
#             <img src="{image_url}" class="admin-image-box" width="50" height="50" load="lazy" /></a>''')


# class RelatedPostInline(SortableInlineAdminMixin, DynamicRawIDMixin, admin.TabularInline):
#     formset = RelatedPostInlineFormset
#     model = RelatedPost
#     fk_name = 'from_post'
#     autocomplete_fields = ('to_post',)
#     classes = ('collapse',)
#     extra = 0
#     ordering = ('display_priority',)


# @admin.register(AbstractBlogPost)
# class PostAdmin(AdminAutoSaveMixin, SortableAdminBase, DynamicRawIDMixin, TranslationAdmin):
#     fieldsets = (
#         (_('پست'), {'fields': (
#             'author', 'category', 'name', 'image',
#         )}),
#         *ContentAdminMixin.fieldsets,
#         *SeoAdminMixin.fieldsets,
#         *DateTimeAdminMixin.fieldsets,
#         (_('تنظیمات بیشتر'), {
#             'fields': ('related_items_display_status', 'autofill_related_items'),
#             'classes': ('collapse',),
#         }),
#     )
#     readonly_fields = (*DateTimeAdminMixin.readonly_fields, 'author',)
#     list_display = ('name', *SeoAdminMixin.list_display, 'display_post_image_thumbnail')
#     list_per_page = 20
#     list_filter = (*SeoAdminMixin.list_filter, 'category',)
#     search_fields = ('name',)
#     prepopulated_fields = {"slug": ("name",)}
#     autocomplete_fields = ('category',)
#     inlines = (RelatedPostInline, *SeoAdminMixin.inlines,)
#     actions = (*SeoAdminMixin.actions,)

# class Media:
#     js = (
#         "admin/blog/js/make_automatic_description.js",
#         "ckeditor/ckeditor/config.js",
#     )
#
# @admin.display(description=_('تصویر'), empty_value='-')
# def display_post_image_thumbnail(self, obj):
#     image_url = obj.get_image
#     return mark_safe(f'''<a target="_blank" href="{image_url}">
#         <img src="{image_url}" class="admin-image-box" width="50" height="50" load="lazy" /></a>''')
#
# # save current user as author
# def save_model(self, request, obj, form, change):
#     if not obj.author:
#         obj.author = request.user
#         obj.save()
#     super().save_model(request, obj, form, change)


# @admin.register(Settings)
class BlogSettingsAdminMixin(admin.ModelAdmin):
    list_display = ('display_page_title',)
    fieldsets = (
        (None, {'fields': ('related_items_display_status', 'related_items_number', 'autofill_related_items')}),
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


class BlogTagAdminMixin(TabbedTranslationAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'name',
            ],
        }),
        *SeoAdminMixin.fieldsets,
        *DateTimeAdminMixin.fieldsets,
    ]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)