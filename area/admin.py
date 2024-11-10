# Django Built-in modules
from django.contrib import admin

# Local apps
from .models import (
    Province,
    City
)
from utils.admin import DateTimeAdminMixin

# Third Party Packages
from modeltranslation.admin import TabbedTranslationAdmin



@admin.register(Province)
class ProvinceAdmin(TabbedTranslationAdmin):
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    search_fields = ('name',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy


@admin.register(City)
class CityAdmin(TabbedTranslationAdmin):
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('name',)
    list_filter = ('province',)
    search_fields = ('name',)
    autocomplete_fields = ('province',)
    date_hierarchy = DateTimeAdminMixin.date_hierarchy
