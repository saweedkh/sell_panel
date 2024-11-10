# Django Built-in modules
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import (
    AbstractBaseSeoModel,
    MetadataModel,
)

# Third Party Packages
from modeltranslation.admin import TranslationGenericTabularInline


class MetadataAdminInline(TranslationGenericTabularInline):
    model = MetadataModel
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 80})
        },
    }
    # classes = ('collapse',)
    extra = 0


class SeoAdminMixin(admin.ModelAdmin):
    fieldsets = (
        (_('گزینه های سئو'), {
            # 'classes': ('collapse',),
            'fields': (
                'slug',
                'page_display_status',
                'search_engine_title',
                'search_engine_description',
                'search_engine_keywords',
                'canonical_link',
            ),
        }),
    )
    list_display = ('page_display_status',)
    list_filter = ('page_display_status',)
    inlines = (MetadataAdminInline,)
    list_editable = ('page_display_status',)

    # Actions
    @admin.action(description=_('تغییر وضعیت نمایش به انتشار'))
    def make_published(modeladmin, request, queryset):
        queryset.update(page_display_status=AbstractBaseSeoModel.PUBLISH)

    @admin.action(description=_('تغییر وضعیت نمایش به پیش نمایش'))
    def make_drafted(modeladmin, request, queryset):
        queryset.update(page_display_status=AbstractBaseSeoModel.DRAFT)

    actions = (make_published, make_drafted)


class ContentAdminMixin(admin.ModelAdmin):
    fieldsets = (
        (_('توضیحات و محتوا'), {
            # 'classes': ('collapse',),
            'fields': ('description', 'content',),
        }),
    )
