# Django Build-in
from django.contrib import admin

# Local Apps
from .models import TranslatorSetting

# Third Party Packages
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(TranslatorSetting)
class TranslatorSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'source_language', 'search_engine', 'active'
        )}),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class TranslatorAdmin(TabbedTranslationAdmin):
    class Media:
        js = ('admin/translator/js/auto_translator.js',)
