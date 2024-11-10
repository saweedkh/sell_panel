# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import (
    Home,
    About,
)
from utils.admin import StaticPageAdminMixin

# Third Party Packages
from modeltranslation.admin import TranslationStackedInline, TabbedTranslationAdmin



@admin.register(Home)
class HomePageAdmin(TabbedTranslationAdmin, StaticPageAdminMixin):
    fieldsets = (
        *StaticPageAdminMixin.fieldsets,
        (_('ویدیو'), {'fields': ('video',)}),
    )
    
    class Media:
        js = (
            "ckeditor/ckeditor/config.js",
        )



@admin.register(About)
class AboutPageAdmin(TabbedTranslationAdmin, StaticPageAdminMixin):
    fieldsets = (
        *StaticPageAdminMixin.fieldsets,
        (_('ویدیو'), {'fields': ('video',)}),
    )
