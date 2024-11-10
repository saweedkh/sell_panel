# Django Built-in modules
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

# Local Apps
from .models import AbstractBaseComment

# Third Party Packages
from dynamic_raw_id.admin import DynamicRawIDMixin


class CommentAdminMixin(DynamicRawIDMixin, admin.ModelAdmin):
    fieldsets = (
        (_('نظرات'), {
            'fields': (
                'parent',
                'user',
                'name',
                'email',
                'review',
                'status',
                'comment_type',
            ),
        }),
    )
    list_display = ('name', 'status')
    list_filter = ('status', 'comment_type',)
    search_fields = ('name', 'review',)
    # autocomplete_fields = ('user', 'parent',)
    dynamic_raw_id_fields = ('user', 'parent',)

    # Actions
    @admin.action(description=_('تغییر وضعیت کامنت به تایید شده'))
    def make_accepted(modeladmin, request, queryset):
        queryset.update(status=AbstractBaseComment.ACCEPT)

    @admin.action(description=_('تغییر وضعیت کامنت به رد شده'))
    def make_declined(modeladmin, request, queryset):
        queryset.update(status=AbstractBaseComment.DECLINE)

    actions = (make_accepted, make_declined)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.order_by('-created')
        return queryset
