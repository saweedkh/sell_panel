# Django Built-in Modules
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Third-party Apps
from mptt.admin import DraggableMPTTAdmin
from dynamic_raw_id.admin import DynamicRawIDMixin
from modeltranslation.admin import TabbedTranslationAdmin

# Local Apps
from .forms import CustomMenuObjectModelForm
from .models import MenuObject
from utils.admin import DateTimeAdminMixin


@admin.register(MenuObject)
class MenuObjectAdmin(DynamicRawIDMixin, DraggableMPTTAdmin, TabbedTranslationAdmin):
    """
        autocomplete_field ``content_type`` need ContentType model admin to be registered along with
        overriding the method ``get_search_results`` in ContentType model admin as below otherwise just
        remove autocomplete_field ``content_type``:

        def get_search_results(self, request, queryset, search_term):
            queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term,)
            if request.GET.get('model_name') == 'menuobject':
                models_with_get_absolute_url = [ctype.id for ctype in ContentType.objects.all() if
                                                hasattr(ctype.model_class(), 'get_absolute_url')]
                queryset = queryset.filter(id__in=models_with_get_absolute_url)
            return queryset, may_have_duplicates

    """
    fieldsets = (
        (None, {'fields': ('name', 'parent', 'url', 'content_type', 'object_id')}),
        *DateTimeAdminMixin.fieldsets,
    )
    form = CustomMenuObjectModelForm
    list_display = ('tree_actions', 'indented_title', 'display_link',
                    *DateTimeAdminMixin.list_display)
    list_display_links = ('indented_title',)
    dynamic_raw_id_fields = ('parent',)
    autocomplete_fields = ('content_type',)
    search_fields = ('name',)
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)

    @admin.display(description=_("عنوان"))
    def indented_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.name,
        )

    @admin.display(description=_("لینک"))
    def display_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.get_link,
            _('نمایش'),
        )


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    """
        to use autocomplete_field ``content_type`` in ``MenuObjectAdmin``, registering this class is necessary
    """
    search_fields = ('app_label', 'model')

    # filter models contain method get_absolute_url()
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )

        # check if autocomplete ajax request has been sent from 'MenuObject' model
        if request.GET.get('model_name') == 'menuobject':
            filtered_models = [
                ctype.id for ctype in ContentType.objects.exclude(app_label='menu')
                if ctype.model_class() in admin.site._registry and hasattr(ctype.model_class(), 'get_absolute_url')
            ]
            queryset = queryset.filter(id__in=filtered_models)
        return queryset, may_have_duplicates
